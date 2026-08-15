<template>
  <div class="upload">
    <div>
      <strong>{{ label }}</strong>
      <p>{{ uploaded ? doneText : helpText }}</p>
    </div>
    <label class="upload-button">
      {{ uploaded ? doneText : uploadText }}
      <input type="file" accept="application/pdf,image/jpeg,image/png" @change="onFileChange" />
    </label>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  label: string;
  uploaded: boolean;
}>();

const emit = defineEmits<{ upload: [file: File] }>();

function onFileChange(event: Event) {
  const input = event.target as HTMLInputElement;
  if (input.files?.[0]) emit("upload", input.files[0]);
}

const uploadText = "Upload";
const doneText = "Done";
const helpText = "Photo or PDF";
</script>
