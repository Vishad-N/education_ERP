<template>
  <div class="shell portal-shell">
    <header class="topbar">
      <div>
        <p class="eyebrow">{{ hi ? "छात्र पोर्टल" : "Student portal" }}</p>
        <h1>{{ hi ? "बच्चे की जानकारी" : "Student and guardian" }}</h1>
      </div>
      <button class="secondary language-toggle" type="button" @click="hi = !hi">
        {{ hi ? "English" : "हिन्दी" }}
      </button>
    </header>

    <main class="portal-content" aria-live="polite">
      <p v-if="loading" class="safe-message">{{ hi ? "जानकारी लोड हो रही है..." : "Loading your information..." }}</p>
      <p v-else-if="error" class="form-error" role="alert">{{ error }}</p>
      <template v-else-if="snapshot">
        <section class="portal-band">
          <p class="eyebrow">{{ hi ? "छात्र" : "Student" }}</p>
          <h2>{{ snapshot.student.student_name }}</h2>
          <p>{{ snapshot.student.name }}</p>
          <p class="safe-message">{{ hi ? "लिंक समाप्ति" : "Access expires" }}: {{ snapshot.expires_on }}</p>
        </section>

        <section class="portal-section">
          <div class="section-heading">
            <h2>{{ hi ? "फीस बाकी" : "Fee dues" }}</h2>
            <span class="count">{{ snapshot.dues.length }}</span>
          </div>
          <p v-if="!snapshot.dues.length" class="muted">{{ hi ? "कोई फीस बाकी नहीं है।" : "No fee dues." }}</p>
          <div v-for="due in snapshot.dues" :key="due.name" class="portal-row">
            <div><strong>{{ due.name }}</strong><span>{{ hi ? "अंतिम तारीख" : "Due" }}: {{ due.due_date }}</span></div>
            <button class="primary compact-button" type="button" @click="paymentAttempts[due.name] ? checkPayment(due.name) : startPayment(due.name)">
              {{ paymentStates[due.name] || (hi ? "भुगतान" : "Pay") }}
            </button>
            <strong>INR {{ due.net_amount }}</strong>
          </div>
        </section>

        <section class="portal-section">
          <div class="section-heading">
            <h2>{{ hi ? "रसीदें" : "Receipts" }}</h2>
            <span class="count">{{ snapshot.receipts.length }}</span>
          </div>
          <p v-if="!snapshot.receipts.length" class="muted">{{ hi ? "अभी कोई रसीद नहीं है।" : "No receipts yet." }}</p>
          <div v-for="receipt in snapshot.receipts" :key="receipt.name" class="portal-row">
            <div><strong>{{ receipt.receipt_no || receipt.name }}</strong><span>{{ receipt.approved_on }}</span></div>
            <button class="secondary compact-button" type="button" @click="downloadReceipt(receipt.name)">
              {{ hi ? "डाउनलोड" : "Download" }}
            </button>
            <strong>INR {{ receipt.amount }}</strong>
          </div>
        </section>

        <section class="portal-section">
          <div class="section-heading">
            <h2>{{ hi ? "सूचनाएं" : "Notices" }}</h2>
            <span class="count">{{ snapshot.notices.length }}</span>
          </div>
          <p v-if="!snapshot.notices.length" class="muted">{{ hi ? "अभी कोई सूचना नहीं है।" : "No notices." }}</p>
          <div v-for="notice in snapshot.notices" :key="notice.name" class="notice-row">
            <strong>{{ notice.title }}</strong>
            <span>{{ notice.message }}</span>
            <small>{{ notice.published_on }}</small>
          </div>
        </section>

        <section class="portal-section">
          <div class="section-heading">
            <h2>{{ hi ? "दस्तावेज़" : "Documents" }}</h2>
            <span class="count">{{ snapshot.documents.length }}</span>
          </div>
          <p v-if="!snapshot.documents.length" class="muted">{{ hi ? "अभी कोई दस्तावेज़ नहीं है।" : "No documents yet." }}</p>
          <div v-for="document in snapshot.documents" :key="document.name" class="portal-row">
            <div><strong>{{ document.document_type }}</strong><span>{{ document.expiry_date || (hi ? "समाप्ति तारीख नहीं" : "No expiry date") }}</span></div>
            <span class="state">{{ document.verification_status }}</span>
          </div>
        </section>
      </template>
    </main>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from "vue";

type Snapshot = {
  expires_on: string;
  student: { name: string; student_name: string; student_email_id: string };
  dues: Array<{ name: string; net_amount: number; due_date: string; status: string }>;
  receipts: Array<{ name: string; amount: number; receipt_no: string; approved_on: string; status: string }>;
  documents: Array<{ name: string; document_type: string; verification_status: string; expiry_date: string }>;
  notices: Array<{ name: string; title: string; message: string; published_on: string; expires_on: string }>;
};

const hi = ref(false);
const loading = ref(true);
const error = ref("");
const snapshot = ref<Snapshot | null>(null);
const paymentStates = ref<Record<string, string>>({});
const paymentAttempts = ref<Record<string, string>>({});

onMounted(async () => {
  const token = new URLSearchParams(window.location.search).get("access") || localStorage.getItem("university_erp_student_access");
  if (!token) {
    error.value = "Open this portal with a valid access link.";
    loading.value = false;
    return;
  }
  localStorage.setItem("university_erp_student_access", token);
  try {
    const response = await fetch("/api/method/university_erp.api.portal.get_student_portal_snapshot", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ access_token: token }),
    });
    const result = await response.json();
    if (!response.ok || result.exc) throw new Error("Portal data could not be loaded.");
    snapshot.value = result.message;
  } catch {
    error.value = "Portal data could not be loaded. Request a new access link.";
  } finally {
    loading.value = false;
  }
});

async function downloadReceipt(receipt: string) {
  const token = localStorage.getItem("university_erp_student_access");
  if (!token) return;
  const response = await fetch("/api/method/university_erp.api.portal.download_student_receipt", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ access_token: token, receipt }),
  });
  if (!response.ok) return;
  const url = URL.createObjectURL(await response.blob());
  const anchor = document.createElement("a");
  anchor.href = url;
  anchor.download = `${receipt}.pdf`;
  anchor.click();
  URL.revokeObjectURL(url);
}

async function startPayment(demand: string) {
  const token = localStorage.getItem("university_erp_student_access");
  if (!token) return;
  const key = `student-payment-${demand}`;
  paymentStates.value[demand] = hi.value ? "लोड हो रहा है" : "Starting...";
  const response = await fetch("/api/method/university_erp.api.portal.create_student_payment", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ access_token: token, student_fee_demand: demand, idempotency_key: key }),
  });
  const result = await response.json();
  if (!response.ok || result.exc) {
    paymentStates.value[demand] = hi.value ? "फिर कोशिश करें" : "Retry";
    return;
  }
  paymentAttempts.value[demand] = result.message.attempt;
  paymentStates.value[demand] = result.message.status === "Paid" ? (hi.value ? "भुगतान हुआ" : "Paid") : `${hi.value ? "आदेश" : "Order"} ${result.message.provider_order_id}`;
}

async function checkPayment(demand: string) {
  const token = localStorage.getItem("university_erp_student_access");
  const attempt = paymentAttempts.value[demand];
  if (!token || !attempt) return;
  const response = await fetch("/api/method/university_erp.api.portal.check_student_payment", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ access_token: token, attempt }),
  });
  const result = await response.json();
  if (!response.ok || result.exc) {
    paymentStates.value[demand] = hi.value ? "फिर कोशिश करें" : "Retry";
    return;
  }
  paymentStates.value[demand] = result.message.status === "Paid" ? (hi.value ? "भुगतान हुआ" : "Paid") : (hi.value ? "स्थिति देखें" : "Check status");
}
</script>
