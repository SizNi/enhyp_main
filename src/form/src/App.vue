<template>
  <form @submit.prevent="submit" class="vue-form">
    <div class="vue-form__section">
      <h1 class="vue-form__title">Скважина</h1>
      <ui-input @change-value="updateForm" :name="key" :label="label" :required="required"
                :error="error"
                type="well"
                layout="grid"
                v-for="({label, required, error}, key) of fields.well"/>
    </div>

    <div class="vue-form__section">
      <div class="vue-form__list">
        <div v-for="(string, index) of fields.casingString" class="vue-form__section">
          <h3 class="vue-form__subtitle">Обсадная колонна № {{ index + 1 }}</h3>
          <div class="vue-form__range-inputs">
            <ui-input @change-value="updateForm" name="diameter" :label="string.diameter.label"
                      :required="string.diameter.required"
                      :error="string.diameter.error"
                      :index="index"
                      type="casingString"
                      layout="grid"
            />

            <div class="vue-form__range-inputs _1">
              <div class="input-label">
                <span>Глубины</span>
              </div>

              <div class="vue-form__range-item">
                <ui-input @change-value="updateForm" :name="name" :label="label" :required="required"
                          :error="error"
                          type="casingString"
                          layout="grid"
                          :index="index"
                          subtype="depth"
                          v-for="({label, required, error}, name) of string.depth"/>
              </div>
            </div>
          </div>
        </div>
        <button @click.prevent="addField('casingString')" class="vue-form__add">+ Добавить обсадную колонну
        </button>
      </div>
    </div>

    <div class="vue-form__section">
      <h3 class="vue-form__subtitle">Фильтровая колонна</h3>
      <div class="vue-form__list">

        <div class="vue-form__select">
          <div class="input-label">
            <span>Тип колонны</span>
            <span class="_color-red">*</span>
          </div>
          <Multiselect
              class="vue-form__select-input"
              v-model="columnTypeValue"
              :filter-results="true"
              :min-chars="1"
              :searchable="true"
              :options="columnTypeOptions"
          />
        </div>

        <ui-input @change-value="updateForm" name="diameter"
                  :label="fields.filterColumn.diameter.label"
                  :required="fields.filterColumn.diameter.required"
                  :error="fields.filterColumn.diameter.error"
                  type="filterColumn"
                  layout="grid"
        />

        <div class="vue-form__range-inputs _1">
          <div class="input-label">
            <span>Глубины</span>
          </div>

          <div class="vue-form__range-item">
            <ui-input @change-value="updateForm" :name="name" :label="label" :required="required"
                      :error="error"
                      type="filterColumn"
                      layout="grid"
                      subtype="depth"
                      v-for="({label, required, error}, name) of fields.filterColumn.depth"/>
          </div>

          <div v-if="fields.filterColumn.intervals.length" class="vue-form__list">
            <div class="input-label">
              <span>Интервал установки фильтра, м</span>
            </div>

            <div v-for="(interval, index) of fields.filterColumn.intervals" class="vue-form__range-item">
              <ui-input @change-value="updateForm" :name="name" :label="label" :required="required"
                        :error="error"
                        type="filterColumn"
                        layout="grid"
                        subtype="intervals"
                        :index="index"
                        v-for="({label, required, error}, name) of interval"/>
            </div>


            <button @click.prevent="addField('filterColumn' ,'intervals')"
                    class="vue-form__add">+ Добавить интервал установки
              фильтра
            </button>
          </div>
        </div>
      </div>
    </div>

    <div class="vue-form__section _borders">
      <h3 class="vue-form__subtitle">Оснастка</h3>
      <div class="vue-form__list _2">
        <ui-input @change-value="updateForm" :name="key" :label="label" :required="required"
                  :error="error"
                  layout="grid"
                  type="rigging"
                  v-for="({label, required, error}, key) of fields.rigging"/>
      </div>
    </div>

    <div class="vue-form__section">
      <h1 class="vue-form__subtitle">Геологическое строение (layers)</h1>

      <div class="vue-form__list">
        <div v-for="(horizon, index) of fields.horizons" class="vue-form__section">
          <h3 class="vue-form__subtitle">Горизонт № {{ index + 1 }}</h3>
          <div class="vue-form__list">
            <ui-input @change-value="updateForm" name="name" :label="horizon.name.label"
                      :required="horizon.name.required"
                      :error="horizon.name.error"
                      :index="index"
                      type="horizons"
                      layout="grid"
            />

            <div class="vue-form__range-inputs _1">
              <div class="input-label">
                <span>Глубины</span>
              </div>

              <div class="vue-form__range-item">
                <ui-input @change-value="updateForm" :name="name" :label="label" :required="required"
                          :error="error"
                          type="horizons"
                          layout="grid"
                          :index="index"
                          subtype="depth"
                          v-for="({label, required, error}, name) of horizon.depth"/>
              </div>
            </div>

            <div class="vue-form__range-inputs _1">
              <div class="input-label">
                <span>Тип отложений</span>
              </div>
              <Multiselect
                  mode="tags"
                  class="vue-form__select-input"
                  v-model="formData.horizons[index].depositType"
                  :filter-results="true"
                  :min-chars="1"
                  :searchable="true"
                  :options="depositTypeOptions"
              />
            </div>

            <div class="vue-form__range-inputs _1">
              <div class="input-label">
                <span>Прослои</span>
              </div>
              <Multiselect
                  mode="tags"
                  class="vue-form__select-input"
                  v-model="formData.horizons[index].interlayers"
                  :filter-results="true"
                  :min-chars="1"
                  :searchable="true"
                  :options="interlayersOptions"
              />
            </div>

            <div class="vue-form__range-inputs _1">
              <div class="input-label">
                <span>Вкрапления</span>
              </div>
              <Multiselect
                  mode="tags"
                  class="vue-form__select-input"
                  v-model="formData.horizons[index].inclusions"
                  :filter-results="true"
                  :min-chars="1"
                  :searchable="true"
                  :options="inclusionsOptions"
              />
            </div>
          </div>
        </div>
        <button @click.prevent="addField('horizons')" class="vue-form__add">+ Добавить горизонт
        </button>
      </div>
    </div>
    <button>Отправить</button>
  </form>
</template>
<script setup>
import Multiselect from '@vueform/multiselect'
import * as yup from "yup";
import UiInput from "./components/ui/Input.vue";
import errors from "@/messages/errors.js";
import {ref, watch} from 'vue';
import axios from "axios";

const columnTypeValue = ref('Открытый ствол');

const columnTypeOptions = ref([
  'Открытый ствол',
  'Фильтровая колонна',
]);

const depositTypeOptions = ref([
    'пески',
    'пески мелкие',
    'пески средние',
    'пески крупные',
    'суглинки',
    'супеси',
    'глины',
    'известняки',
    'мергели',
    'песчаники',
    'доломиты',
    'мел',
    'гнейсы',
    'граниты',
]);

const interlayersOptions = ref([
  'пески',
  'пески мелкие',
  'пески средние',
  'пески крупные',
  'суглинки',
  'супеси',
  'глины',
  'известняки',
  'мергели',
  'песчаники',
  'доломиты',
  'мел',
  'гнейсы',
  'граниты',
]);

const inclusionsOptions = ref([
  'глыбы',
  'валуны',
  'галька',
  'щебень',
  'гравий',
  'фосфориты(в подошве слоя)',
]);

const getDefaultForm = {
  horizons: () => ({
    depositType: [],
    interlayers: [],
    inclusions: [],
  })
};

const getDefaultField = {
  from: () => ({
    label: "От, м",
    required: true,
  }),
  to: () => ({
    label: "До, м",
    required: true,
  }),
  casingString: () => ({
    diameter: {
      label: "Диаметр колонны, мм",
      required: true,
    },
    depth: getDefaultField.range(),
  }),
  horizon: () => ({
    name: {
      label: "Индекс (name)",
      required: true,
    },
    depth: getDefaultField.range(),
    depositType: [],
    interlayers: [],
    inclusions: []
  }),
  range: () => ({
    from: getDefaultField.from(),
    to: getDefaultField.to(),
  })
};

const getDefaultValidationRule = {
  casingString: (id) => [
    [`casingString-string-${id}-diameter`, yup.string().required(errors.required)],
    [`casingString-string-${id}-depth-from`, yup.string().required(errors.required)],
    [`casingString-string-${id}-depth-to`, yup.string().required(errors.required)],
  ],
  horizon: (id) => [
    [`horizons-horizon-${id}-name`, yup.string().required(errors.required)],
    [`horizons-horizon-${id}-depth-from`, yup.string().required(errors.required)],
    [`horizons-horizon-${id}-depth-to`, yup.string().required(errors.required)],
  ],
  filterColumnRange: () => [
    [`filterColumn-depth-from`, yup.string().required(errors.required)],
    [`filterColumn-depth-to`, yup.string().required(errors.required)],
  ],
  filterColumnInterval: (id) => [
    [`filterColumn-intervals-${id}-from`, yup.string().required(errors.required)],
    [`filterColumn-intervals-${id}-to`, yup.string().required(errors.required)],
  ]
};

const fields = ref({
  well: {
    depth: {
      label: "Глубина скважины, м",
      required: true,
    }
  },
  casingString: [getDefaultField.casingString()],
  filterColumn: {
    diameter: {
      label: "Диаметр колонны, мм",
      required: true,
    },
    depth: getDefaultField.range(),
    intervals: [],
  },
  rigging: {
    pumpName: {
      label: "Название насоса",
      required: false,
    },
    pumpDepth: {
      label: "Глубина установки насоса, м",
      required: false,
    },
    staticLvl: {
      label: "Статический уровень, м",
      required: false,
    },
    dynamicLvl: {
      label: "Динамический уровень, м",
      required: false,
    }
  },
  horizons: [getDefaultField.horizon()]
});

const validationState = ref(false);
const formData = ref({
  filterColumn: {
    type: columnTypeValue.value
  },
  horizons: [
    getDefaultForm.horizons(),
  ]
});

const validationMap = new Map([
  ['well-depth', yup.string().required(errors.required)],
  [`filterColumn-diameter`, yup.string().required(errors.required)],
  ...getDefaultValidationRule.casingString(1),
  ...getDefaultValidationRule.filterColumnRange(1),
  ...getDefaultValidationRule.horizon(1)
]);


const validFields = new Set();
const validIndex = ref(validationMap.size);
const validateForm = () => {
  validationState.value = validFields.size === validIndex.value;
};

const setError = (type, subtype, name, index, error) => {
  let currentInput = null;

  switch (type) {
    case "well": {
      currentInput = fields.value[type][name];
      break;
    }

    case "casingString": {
      if (subtype === 'depth') {
        currentInput = fields.value[type][index][subtype][name];
        break;
      }
      currentInput = fields.value[type][index][name];
      break;
    }

    case "horizons": {
      if (subtype === 'depth') {
        currentInput = fields.value[type][index][subtype][name];
        break;
      }
      currentInput = fields.value[type][index][name];
      break;
    }

    case "filterColumn": {
      if (subtype === 'depth') {
        currentInput = fields.value[type][subtype][name];
        break;
      } else if (subtype === 'intervals') {
        currentInput = fields.value[type][subtype][index][name];
        break;
      }

      currentInput = fields.value[type][name];
      break;
    }
  }

  currentInput['error'] = error;
}

const updateForm = ({name, value, type, subtype, index}) => {
  let validationRule = "";
  switch (type) {
    case "well": {
      if (!Object.hasOwn(formData.value, type)) {
        formData.value[type] = {}
      }

      formData.value[type][name] = value;
      validationRule = `${type}-${name}`;
      break;
    }

    case "casingString": {
      if (!Object.hasOwn(formData.value, type)) {
        formData.value[type] = []
      }

      if (!formData.value[type][index]) {
        formData.value[type][index] = {};
      }

      if (subtype === 'depth') {
        if (!Object.hasOwn(formData.value[type][index], subtype)) {
          formData.value[type][index][subtype] = {};
        }


        formData.value[type][index][subtype][name] = value;
        validationRule = `${type}-string-${index + 1}-${subtype}-${name}`;
        break;
      }

      validationRule = `${type}-string-${index + 1}-${name}`;
      formData.value[type][index][name] = value;
      break;
    }

    case "horizons": {
      if (!Object.hasOwn(formData.value, type)) {
        formData.value[type] = []
      }

      if (!formData.value[type][index]) {
        formData.value[type][index] = {};
      }

      if (subtype === 'depth') {
        if (!Object.hasOwn(formData.value[type][index], subtype)) {
          formData.value[type][index][subtype] = {};
        }

        formData.value[type][index][subtype][name] = value;
        validationRule = `${type}-horizon-${index + 1}-${subtype}-${name}`;
        break;
      }

      validationRule = `${type}-horizon-${index + 1}-${name}`;
      formData.value[type][index][name] = value;
      break;
    }

    case "filterColumn": {
      if (!Object.hasOwn(formData.value, type)) {
        formData.value[type] = {}
      }

      if (subtype === 'depth') {

        if (!Object.hasOwn(formData.value[type], subtype)) {
          formData.value[type][subtype] = {};
        }

        formData.value[type][subtype][name] = value;
        validationRule = `${type}-${subtype}-${name}`;
        break;

      } else if (subtype === 'intervals') {

        if (!Object.hasOwn(formData.value[type], subtype)) {
          formData.value[type][subtype] = [];
        }

        if (!formData.value[type][subtype][index]) {
          formData.value[type][subtype][index] = {};
        }

        formData.value[type][subtype][index][name] = value;

        validationRule = `${type}-${subtype}-${index + 1}-${name}`;
        break;
      }

      validationRule = `${type}-${name}`;
      formData.value[type][name] = value;
      break;
    }
  }

  const validationSchema = validationMap.get(validationRule);

  if (!validationSchema) {
    validateForm();
    return;
  }

  try {
    validationSchema.validateSync(value);
    validFields.add(name);
    setError(type, subtype, name, index, null);
  } catch (e) {
    const [error] = e.errors;
    validFields.has(name) && validFields.delete(name);
    setError(type, subtype, name, index, error);
  } finally {
    validateForm();
  }
};

const removeField = (type, subtype = null) => {
  switch (type) {
    case "filterColumn": {
      fields.value[type][subtype].forEach((_, index) => {
        validationMap.delete(`filterColumn-intervals-${index + 1}-from`)
        validationMap.delete(`filterColumn-intervals-${index + 1}-to`)
      });

      fields.value[type][subtype] = [];
      formData.value[type][subtype] = [];

      validIndex.value = validationMap.size;
      break;
    }
  }
};

const addField = (type, subtype = null) => {
  const currentObject = subtype ? fields.value[type][subtype] : fields.value[type];
  let nextId = currentObject.length + 1;

  switch (type) {
    case "casingString": {
      currentObject.push(getDefaultField.casingString());
      getDefaultValidationRule.casingString(nextId).forEach(([key, value]) => {
        validationMap.set(key, value)
      });
      break;
    }

    case "filterColumn": {
      currentObject.push(getDefaultField.range());
      getDefaultValidationRule.filterColumnInterval(nextId).forEach(([key, value]) => {
        validationMap.set(key, value)
      });
      break;
    }

    case "horizons": {
      currentObject.push(getDefaultField.horizon());
      formData.value.horizons.push(getDefaultForm.horizons());
      getDefaultValidationRule.horizon(nextId).forEach(([key, value]) => {
        validationMap.set(key, value)
      });
      break;
    }
  }

  validIndex.value = validationMap.size;
};


const submit = () => {
  axios.post('/well_section/create/', formData.value)
    .then(response => {
      window.location.href=response.data.url
      console.log(response.data, 'success');
    })
    .catch(error => {
      console.error(error);
    });
};

watch(columnTypeValue, (value) => {
  if (value === 'Открытый ствол' || !value) {
    removeField("filterColumn", "intervals")
  } else {
    addField("filterColumn", "intervals");
  }

  formData.value.filterColumn.type = value;
});

</script>
<style lang="scss">
@import "@vueform/multiselect/themes/default.css";

.vue-form {
  & * {
    padding: 0;
    margin: 0;
    box-sizing: border-box;
  }

  display: grid;
  grid-gap: 2rem;
  justify-content: center;
  box-sizing: border-box;
  width: 100%;
  padding: 3rem;


  &__select {
    display: grid;
    grid-gap: .8rem;
    grid-template-rows: auto 1fr;
    min-width: 15rem;
  }

  &__range-inputs {
    display: grid;
    grid-gap: .8rem;
    align-items: start;

    &._1 {
      grid-template-columns: auto;
      grid-auto-flow: row;
    }

    &._2 {
      display: grid;
      grid-template-columns: auto auto;
      grid-auto-flow: row;
    }

    &._3 {
      display: flex;
    }

  }

  &__section {
    display: grid;
    grid-gap: .8rem;
    justify-content: start;

    &._borders {
      padding: 2rem 0;
      border-top: .1rem solid grey;
      border-bottom: .1rem solid grey;
    }
  }

  &__dynamic-list {
    display: grid;
    align-content: start;
    align-items: start;
    justify-items: center;
    justify-content: start;
    grid-column: 1 / -1;
  }

  &__list {
    display: grid;
    grid-gap: 1.2rem;

    &._2 {
      grid-template-columns: auto auto;
    }
  }

  &__range-item {
    display: flex;
    grid-gap: .8rem;
  }
}
</style>
