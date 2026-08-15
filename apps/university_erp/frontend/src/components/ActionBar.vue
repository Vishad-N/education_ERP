<template>
  <div class="actions">
    <button v-if="showBack" class="secondary" type="button" @click="$emit('back')">
      {{ backLabel }}
    </button>
    <button class="primary" type="button" @click="$emit('next')">
      {{ nextLabel }}
    </button>
  </div>
</template>

<script setup lang="ts">
withDefaults(
  defineProps<{
    backLabel: string;
    nextLabel: string;
    showBack?: boolean;
  }>(),
  { showBack: true },
);

defineEmits<{
  back: [];
  next: [];
}>();
</script>
