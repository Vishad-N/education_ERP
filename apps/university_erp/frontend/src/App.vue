<template>
  <div class="shell" :lang="language">
    <header class="topbar">
      <div>
        <p class="eyebrow">{{ t.portal }}</p>
        <h1>{{ t.title }}</h1>
      </div>
      <div class="language" aria-label="Language">
        <button
          :class="{ active: language === 'en' }"
          type="button"
          @click="language = 'en'"
        >
          English
        </button>
        <button
          :class="{ active: language === 'hi' }"
          type="button"
          @click="language = 'hi'"
        >
          हिन्दी
        </button>
      </div>
    </header>

    <main class="layout">
      <nav class="steps" aria-label="Application steps">
        <button
          v-for="step in steps"
          :key="step.id"
          :class="{ active: activeStep === step.id, done: isDone(step.id) }"
          type="button"
          :aria-current="activeStep === step.id ? 'step' : undefined"
          @click="goToStep(step.id)"
        >
          <span class="step-icon" aria-hidden="true">{{ step.icon }}</span>
          <span>{{ label(step.label) }}</span>
        </button>
      </nav>

      <section class="panel" aria-live="polite">
        <div class="status-row">
          <span :class="['network', online ? 'online' : 'offline']">
            {{ online ? t.online : t.offline }}
          </span>
          <span>{{ t.saved }} {{ savedAt }}</span>
          <span v-if="syncState === 'synced'">{{ t.synced }}</span>
          <span v-else-if="syncState === 'syncing'">{{ t.syncing }}</span>
          <span v-else-if="syncState === 'error'">{{ t.syncError }}</span>
        </div>
        <p v-if="formError" class="form-error" role="alert">{{ formError }}</p>

        <form v-if="activeStep === 'register'" class="form" @submit.prevent="next">
          <h2>{{ t.registerTitle }}</h2>
          <label>
            {{ t.mobile }}
            <input
              v-model="application.mobile"
              inputmode="tel"
              maxlength="10"
              placeholder="9876543210"
            />
          </label>
          <label>
            {{ t.guardianName }}
            <input v-model="application.guardianName" autocomplete="name" />
          </label>
          <label>
            {{ t.childName }}
            <input v-model="application.childName" />
          </label>
          <ActionBar :back-label="t.back" :next-label="t.next" :show-back="false" @next="next" />
        </form>

        <form v-else-if="activeStep === 'program'" class="form" @submit.prevent="next">
          <h2>{{ t.programTitle }}</h2>
          <label>
            {{ t.classApplying }}
            <select v-model="application.classApplying">
              <option value="Class 6">{{ t.class6 }}</option>
              <option value="Class 7">{{ t.class7 }}</option>
              <option value="Class 8">{{ t.class8 }}</option>
              <option value="Class 9">{{ t.class9 }}</option>
            </select>
          </label>
          <label>
            {{ t.previousSchool }}
            <input v-model="application.previousSchool" />
          </label>
          <ActionBar :back-label="t.back" :next-label="t.next" @back="back" @next="next" />
        </form>

        <form v-else-if="activeStep === 'application'" class="form" @submit.prevent="next">
          <h2>{{ t.applicationTitle }}</h2>
          <label>
            {{ t.dateOfBirth }}
            <input v-model="application.dateOfBirth" type="date" />
          </label>
          <label>
            {{ t.address }}
            <textarea v-model="application.address" rows="3"></textarea>
          </label>
          <label class="checkbox">
            <input v-model="application.consent" type="checkbox" />
            <span>{{ t.consent }}</span>
          </label>
          <ActionBar :back-label="t.back" :next-label="t.next" @back="back" @next="next" />
        </form>

        <form v-else-if="activeStep === 'documents'" class="form" @submit.prevent="next">
          <h2>{{ t.documentsTitle }}</h2>
          <DocumentUpload
            :label="t.birthCertificate"
            :uploaded="application.birthCertificate"
            @upload="uploadDocument('Birth certificate', $event)"
          />
          <DocumentUpload
            :label="t.photo"
            :uploaded="application.photo"
            @upload="uploadDocument('Child photo', $event)"
          />
          <ActionBar :back-label="t.back" :next-label="t.next" @back="back" @next="next" />
        </form>

        <section v-else-if="activeStep === 'payment'" class="form">
          <h2>{{ t.paymentTitle }}</h2>
          <template v-if="!feeRequired">
            <p class="safe-message">{{ t.paymentWaived }}</p>
          </template>
          <template v-else>
            <div class="amount">
              <span>{{ t.applicationFee }}</span>
              <strong>₹500</strong>
            </div>
            <p class="safe-message">{{ t.paymentSafety }}</p>
            <button class="primary" type="button" @click="markPaid">
              {{ application.paid ? t.paymentDone : paymentPending ? t.paymentPending : t.payNow }}
            </button>
            <button v-if="paymentPending && !application.paid" class="secondary" type="button" @click="checkPayment">
              {{ t.checkPayment }}
            </button>
          </template>
          <ActionBar :back-label="t.back" :next-label="t.next" @back="back" @next="next" />
        </section>

        <section v-else class="form">
          <h2>{{ t.statusTitle }}</h2>
          <div class="summary">
            <p><strong>{{ t.childName }}:</strong> {{ application.childName || "-" }}</p>
            <p><strong>{{ t.classApplying }}:</strong> {{ application.classApplying }}</p>
            <p><strong>{{ t.documents }}:</strong> {{ documentsReady ? t.complete : t.pending }}</p>
            <p><strong>{{ t.payment }}:</strong> {{ application.paid ? t.complete : t.pending }}</p>
          </div>
          <p class="safe-message">{{ t.statusMessage }}</p>
          <ActionBar :back-label="t.back" :next-label="t.finish" @back="back" @next="finish" />
        </section>
      </section>
    </main>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, reactive, ref, watch } from "vue";
import ActionBar from "./components/ActionBar.vue";
import DocumentUpload from "./components/DocumentUpload.vue";
import { messages, type Language } from "./i18n";

type StepId = "register" | "program" | "application" | "documents" | "payment" | "status";

const steps: Array<{ id: StepId; icon: string; label: keyof typeof messages.en }> = [
  { id: "register", icon: "☎", label: "register" },
  { id: "program", icon: "▣", label: "program" },
  { id: "application", icon: "✎", label: "application" },
  { id: "documents", icon: "▤", label: "documents" },
  { id: "payment", icon: "₹", label: "payment" },
  { id: "status", icon: "✓", label: "status" },
];

const language = ref<Language>("en");
const activeStep = ref<StepId>("register");
const savedAt = ref("--:--");
const online = ref(true);
const syncState = ref<"local" | "syncing" | "synced" | "error">("local");
const formVersion = ref("");
const resumeToken = ref("");
const paymentPending = ref(false);
const feeRequired = ref(false);
const formError = ref("");
let syncTimer: ReturnType<typeof setTimeout> | undefined;

const application = reactive({
  mobile: "",
  guardianName: "",
  childName: "",
  classApplying: "Class 6",
  previousSchool: "",
  dateOfBirth: "",
  address: "",
  consent: false,
  birthCertificate: false,
  photo: false,
  paid: false,
});

const t = computed(() => messages[language.value]);
const documentsReady = computed(() => application.birthCertificate && application.photo);

function label(key: keyof typeof messages.en) {
  return messages[language.value][key];
}

function stepIndex(id: StepId) {
  return steps.findIndex((step) => step.id === id);
}

function isDone(id: StepId) {
  return stepIndex(id) < stepIndex(activeStep.value);
}

function goToStep(id: StepId) {
  if (stepIndex(id) <= stepIndex(activeStep.value)) activeStep.value = id;
}

function next() {
  formError.value = "";
  if (activeStep.value === "register" && (!/^\d{10}$/.test(application.mobile) || !application.guardianName || !application.childName)) {
    formError.value = t.value.requiredRegister;
    return;
  }
  if (activeStep.value === "application" && (!application.dateOfBirth || !application.address || !application.consent)) {
    formError.value = t.value.requiredApplication;
    return;
  }
  if (activeStep.value === "documents" && !documentsReady.value) {
    formError.value = t.value.requiredDocuments;
    return;
  }
  if (activeStep.value === "payment") {
    if (!feeRequired.value) {
      application.paid = true;
    } else if (!application.paid) {
      formError.value = t.value.requiredPayment;
      return;
    }
  }
  const index = stepIndex(activeStep.value);
  activeStep.value = steps[Math.min(index + 1, steps.length - 1)].id;
}

function back() {
  const index = stepIndex(activeStep.value);
  activeStep.value = steps[Math.max(index - 1, 0)].id;
}

async function markPaid() {
  if (!resumeToken.value) await syncDraft();
  if (!resumeToken.value) return;
  try {
    const response = await fetch("/api/method/university_erp.api.portal.create_application_payment", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        resume_token: resumeToken.value,
        idempotency_key: `payment-${resumeToken.value.slice(0, 24)}-application-fee`,
        amount: 500,
      }),
    });
    const result = await response.json();
    if (!response.ok || result.exc) throw new Error("Payment attempt failed");
    paymentPending.value = true;
    syncState.value = "synced";
  } catch {
    syncState.value = "error";
  }
}

async function checkPayment() {
  if (!resumeToken.value) return;
  const idempotencyKey = `payment-${resumeToken.value.slice(0, 24)}-application-fee`;
  try {
    const statusResponse = await fetch("/api/method/university_erp.api.portal.check_application_payment", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        resume_token: resumeToken.value,
        idempotency_key: idempotencyKey,
      }),
    });
    const statusResult = await statusResponse.json();
    if (!statusResponse.ok || statusResult.exc) throw new Error("Payment status failed");
    if (statusResult.message.status !== "Paid" && statusResult.message.provider_order_id) {
      const confirmResponse = await fetch("/api/method/university_erp.api.portal.confirm_application_payment", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          resume_token: resumeToken.value,
          idempotency_key: idempotencyKey,
          provider_order_id: statusResult.message.provider_order_id,
        }),
      });
      const confirmResult = await confirmResponse.json();
      if (!confirmResponse.ok || confirmResult.exc) throw new Error("Payment confirm failed");
      application.paid = confirmResult.message.status === "Paid";
    } else {
      application.paid = statusResult.message.status === "Paid";
    }
    paymentPending.value = !application.paid;
  } catch {
    syncState.value = "error";
  }
}

function finish() {
  activeStep.value = "status";
}

function saveDraft() {
  localStorage.setItem(
    "university_erp_guardian_application",
    JSON.stringify({
      language: language.value,
      activeStep: activeStep.value,
      application,
      formVersion: formVersion.value,
      resumeToken: resumeToken.value,
    }),
  );
  savedAt.value = new Intl.DateTimeFormat(language.value === "hi" ? "hi-IN" : "en-IN", {
    hour: "2-digit",
    minute: "2-digit",
  }).format(new Date());
}

async function syncDraft() {
  if (!online.value || !application.mobile || !application.guardianName || !application.childName) return;
  syncState.value = "syncing";
  try {
    const response = await fetch("/api/method/university_erp.api.portal.save_application_draft", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        payload: JSON.stringify({ ...application, formVersion: formVersion.value }),
        resume_token: resumeToken.value || undefined,
        form_version: formVersion.value || undefined,
      }),
    });
    const result = await response.json();
    if (!response.ok || result.exc) throw new Error("Draft sync failed");
    const data = result.message;
    formVersion.value = data.form_version;
    resumeToken.value = data.resume_token || resumeToken.value;
    syncState.value = "synced";
    saveDraft();
  } catch {
    syncState.value = "error";
  }
}

function scheduleSync() {
  saveDraft();
  if (syncTimer) clearTimeout(syncTimer);
  syncTimer = setTimeout(syncDraft, 650);
}

function fileAsBase64(file: File) {
  return new Promise<string>((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = () => resolve(String(reader.result).split(",")[1] || "");
    reader.onerror = () => reject(reader.error);
    reader.readAsDataURL(file);
  });
}

async function uploadDocument(documentType: string, file: File) {
  if (!resumeToken.value) await syncDraft();
  if (!resumeToken.value) {
    formError.value = t.value.uploadFailed;
    return;
  }
  try {
    const response = await fetch("/api/method/university_erp.api.portal.upload_application_document", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        resume_token: resumeToken.value,
        document_type: documentType,
        file_name: file.name,
        content_base64: await fileAsBase64(file),
        idempotency_key: `upload-${resumeToken.value.slice(0, 12)}-${documentType.replaceAll(" ", "-").toLowerCase()}`,
      }),
    });
    const result = await response.json();
    if (!response.ok || result.exc || result.message?.scan_status !== "Scan Passed") {
      formError.value = t.value.uploadFailed;
      throw new Error("Upload failed");
    }
    if (documentType === "Birth certificate") application.birthCertificate = true;
    if (documentType === "Child photo") application.photo = true;
  } catch {
    syncState.value = "error";
  }
}

onMounted(() => {
  const saved = localStorage.getItem("university_erp_guardian_application");
  if (saved) {
    const draft = JSON.parse(saved);
    Object.assign(application, draft.application);
    language.value = draft.language;
    activeStep.value = draft.activeStep;
    formVersion.value = draft.formVersion || "";
    resumeToken.value = draft.resumeToken || "";
  }
  fetch("/api/method/university_erp.api.portal.get_application_context", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: "{}",
  })
    .then((response) => response.json())
    .then((result) => {
      feeRequired.value = Boolean(result.message?.application_fee?.required);
      if (!feeRequired.value) application.paid = true;
    })
    .catch(() => {
      feeRequired.value = false;
      application.paid = true;
    });
  online.value = navigator.onLine;
  window.addEventListener("online", () => (online.value = true));
  window.addEventListener("offline", () => (online.value = false));
  saveDraft();
  syncDraft();
});

watch([application, language, activeStep], scheduleSync, { deep: true });
</script>
