import i18n from "i18next";
import { initReactI18next } from "react-i18next";


// Importing translation files

import translationMG from "./locales/mg/translation.json";
import translationFR from "./locales/fr/translation.json";
import translationEN from "./locales/en/translation.json";


//Creating object with the variables of imported translation files
const resources = {
  mg: {
    translation: translationMG,
  },
  fr: {
    translation: translationFR,
  },
  en: {
    translation: translationEN,
  },
};

//i18N Initialization

i18n
  .use(initReactI18next)
  .init({
    resources,
    lng:"fr", //default language
    keySeparator: false,
    interpolation: {
      escapeValue: false,
    },
  });

export default i18n;