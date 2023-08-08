<template>
  <label class="input-field" :class="`_${layout}`">
    <div v-if="label" class="input-label">
      <span>{{ label }}</span>
      <span v-if="required" class="_color-red">*</span>
    </div>
    <input
        :name="name"
        id="input"
        :placeholder="placeholder"
        v-model="value"
        ref="input"
        class="input"
        :class="{'_error': !!error}"
        @input="emit('change-value', {name, value, type, subtype, index})"
    />
    <transition appear>
      <div v-if="error" class="input-error">{{ error }}</div>
    </transition>
  </label>

</template>

<script setup lang="ts">
import {defineEmits, defineProps, ref} from "vue";

const props = defineProps({
  label: {
    type: String,
    default: ""
  },
  layout: {
    type: String,
    default: "flex"
  },
  required: {
    type: Boolean,
    default: false
  },
  placeholder: {
    type: String,
    default: ""
  },
  name: {
    type: String,
  },
  index: {
    type: Number || undefined,
  },
  error: {
    type: String || null,
    default: null,
  },
  type: {
    type: String,
    default: "",
  },
  subtype: {
    type: String,
    default: "",
  }
});

const value = ref('');
const emit = defineEmits(['change-value']);
const input = ref();
</script>

<style lang="scss" scoped>
input {
  outline: unset;

  &:focus {
    outline: unset;
  }
}

.input {
  padding: 1.2rem;
  color: black;
  border: .1rem solid grey;
  border-radius: 2px;
  transition: border-color .3s, color .3s;

  &::placeholder {
    color: grey;
    font-weight: 400;
    transition: color .3s;
  }

  &._error {
    border-color: red;
    color: red;

    &::placeholder {
      color: red;
    }
  }

}

.input-label {
  display: flex;
  align-items: center;
  font-weight: 400;
  color: black;
}

.input-field {

  &._grid {
    display: grid;
    grid-gap: .8rem;
  }

  &._flex {
    display: flex;
    grid-gap: 1.5rem;
  }

  position: relative;

}

.input-error {
  position: absolute;
  bottom: 0;
  left: 1.2rem;
  color: red;
}

.v-enter-active,
.v-leave-active {
  transition: opacity .5s ease;
}

.v-enter-from,
.v-leave-to {
  opacity: 0;
}
</style>