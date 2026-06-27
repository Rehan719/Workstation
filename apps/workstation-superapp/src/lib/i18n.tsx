import { useCallback, useEffect, useState } from 'react';
import { getPrefs } from './userPrefs';

// E7 (full-UI i18n, increment 1) — a lightweight, dependency-free translation layer. Strings are keyed;
// each language provides what it has, and ANYTHING missing falls back to English (honest: partial coverage
// degrades gracefully to English, never to a blank or a key). The active language follows the user's
// preference (userPrefs.language, BCP-47 → base code). RTL languages flip text direction.
//
// Translations below are for short, standard UI chrome (front door + section headers). Product/proper
// nouns are intentionally kept in English. Coverage is rolled out incrementally surface-by-surface.

type Dict = Record<string, string>;

const RTL = new Set(['ar', 'ur', 'fa', 'he']);
export const baseLang = (code?: string) => (code || 'en').split('-')[0].toLowerCase();
export const isRTL = (code?: string) => RTL.has(baseLang(code));

const en: Dict = {
  'home.eyebrow': 'Workstation IDBO · Command Center',
  'home.title.concept': 'Concept',
  'home.title.commercialisation': 'Commercialisation',
  'home.welcome': 'Welcome',
  'home.intro': 'AI-mediated, on Workstation’s own native AI.',
  'home.intro.work': 'Work in your domain now',
  'home.intro.or': 'or',
  'home.intro.build': 'build a living enterprise',
  'home.intro.tail': 'that runs itself.',
  'home.searchMesh': 'Search Mesh',
  'home.consultCEO': 'Consult CEO',
  'home.journey1.eyebrow': 'Offering 1 · Work now',
  'home.journey1.title': 'Work in a Domain',
  'home.journey1.cta': 'Open Domains',
  'home.journey2.eyebrow': 'Offering 2 · Build an enterprise',
  'home.journey2.title': 'Concept → Commercialisation',
  'home.journey2.cta': 'Start a Genesis',
  'home.platform': 'The Platform',
  'home.recent': 'Continue · Recent work',
  'home.myWork': 'My Work',
  'home.organism': 'Living Organism',
  'home.openOrganism': 'Open Organism',
};

const ar: Dict = {
  'home.eyebrow': 'وركستيشن IDBO · مركز القيادة',
  'home.title.concept': 'الفكرة',
  'home.title.commercialisation': 'التسويق التجاري',
  'home.welcome': 'مرحباً',
  'home.intro': 'بوساطة الذكاء الاصطناعي، على الذكاء الاصطناعي الأصلي الخاص بوركستيشن.',
  'home.intro.work': 'اعمل في مجالك الآن',
  'home.intro.or': 'أو',
  'home.intro.build': 'ابنِ مؤسسة حية',
  'home.intro.tail': 'تدير نفسها بنفسها.',
  'home.searchMesh': 'بحث في الشبكة',
  'home.consultCEO': 'استشر الرئيس التنفيذي',
  'home.journey1.eyebrow': 'العرض 1 · اعمل الآن',
  'home.journey1.title': 'اعمل في مجال',
  'home.journey1.cta': 'افتح المجالات',
  'home.journey2.eyebrow': 'العرض 2 · ابنِ مؤسسة',
  'home.journey2.title': 'الفكرة ← التسويق التجاري',
  'home.journey2.cta': 'ابدأ رحلة جينيسيس',
  'home.platform': 'المنصّة',
  'home.recent': 'تابع · أعمالك الأخيرة',
  'home.myWork': 'أعمالي',
  'home.organism': 'الكائن الحي',
  'home.openOrganism': 'افتح الكائن الحي',
  'navsec.home-facet': 'الرئيسية', 'navsec.domains-facet': 'المجالات', 'navsec.vsb-facet': 'مؤسسات VSB',
  'navsec.econ-facet': 'التحوّل والاقتصاد', 'navsec.gov-facet': 'الحوكمة والثقة', 'navsec.dev-facet': 'المطوّر والنظام',
  'navsec.work-facet': 'العمل في مجال', 'navsec.build-facet': 'بناء مؤسسة', 'navsec.platform-facet': 'المنصّة', 'navsec.system-facet': 'النظام',
  'nav.dashboard': 'لوحة التحكم', 'nav.my-work': 'أعمالي', 'nav.organism': 'الكائن الحي', 'nav.projects': 'المشاريع',
  'nav.marketplace': 'السوق', 'nav.wallet': 'المحفظة', 'nav.deliverables': 'المُخرجات', 'nav.compliance': 'الامتثال',
  'nav.constitution': 'الدستور', 'nav.settings': 'الإعدادات', 'nav.domains': 'نظرة عامة',
  'nav.religion': 'الدين', 'nav.science': 'العلوم', 'nav.education': 'التعليم', 'nav.law': 'القانون', 'nav.care': 'الرعاية', 'nav.employment': 'التوظيف',
  'domains.eyebrow': 'وركستيشن IDBO · العرض 1', 'domains.title': 'المجالات',
  'domains.intro.lead': 'أدوات وموارد خاصة بالمجال بوساطة الذكاء الاصطناعي',
  'domains.off1.tag': 'العرض 1 · أنت هنا', 'domains.off1.title': 'اعمل الآن بأدوات المجال',
  'domains.off2.tag': 'العرض 2', 'domains.off2.title': 'أنشئ مؤسسة حية',
  'domains.six': 'المجالات الستة', 'domains.browseAll': 'تصفّح كل', 'domains.tools': 'أدوات', 'domains.open': 'افتح',
};

const fr: Dict = {
  'home.eyebrow': 'Workstation IDBO · Centre de Commande',
  'home.title.concept': 'Concept',
  'home.title.commercialisation': 'Commercialisation',
  'home.welcome': 'Bienvenue',
  'home.intro': 'Médié par l’IA, sur l’IA native de Workstation.',
  'home.intro.work': 'Travaillez dans votre domaine maintenant',
  'home.intro.or': 'ou',
  'home.intro.build': 'créez une entreprise vivante',
  'home.intro.tail': 'qui se gère elle-même.',
  'home.searchMesh': 'Rechercher',
  'home.consultCEO': 'Consulter le PDG',
  'home.journey1.eyebrow': 'Offre 1 · Travaillez maintenant',
  'home.journey1.title': 'Travailler dans un Domaine',
  'home.journey1.cta': 'Ouvrir les Domaines',
  'home.journey2.eyebrow': 'Offre 2 · Créez une entreprise',
  'home.journey2.title': 'Concept → Commercialisation',
  'home.journey2.cta': 'Démarrer un Genesis',
  'home.platform': 'La Plateforme',
  'home.recent': 'Continuer · Travaux récents',
  'home.myWork': 'Mon Travail',
  'home.organism': 'Organisme Vivant',
  'home.openOrganism': 'Ouvrir l’Organisme',
  // nav sections
  'navsec.home-facet': 'Accueil', 'navsec.domains-facet': 'Domaines', 'navsec.vsb-facet': 'Entreprises VSB',
  'navsec.econ-facet': 'Transformation & Économie', 'navsec.gov-facet': 'Gouvernance & Confiance', 'navsec.dev-facet': 'Développeur & Système',
  'navsec.work-facet': 'Travailler dans un domaine', 'navsec.build-facet': 'Créer une entreprise', 'navsec.platform-facet': 'Plateforme', 'navsec.system-facet': 'Système',
  // nav items (generic + domains; product names fall back to English)
  'nav.dashboard': 'Tableau de bord', 'nav.my-work': 'Mon Travail', 'nav.organism': 'Organisme', 'nav.projects': 'Projets',
  'nav.marketplace': 'Marché', 'nav.wallet': 'Portefeuille', 'nav.deliverables': 'Livrables', 'nav.compliance': 'Conformité',
  'nav.constitution': 'Constitution', 'nav.settings': 'Paramètres', 'nav.domains': 'Aperçu',
  'nav.religion': 'Religion', 'nav.science': 'Science', 'nav.education': 'Éducation', 'nav.law': 'Droit', 'nav.care': 'Soins', 'nav.employment': 'Emploi',
  // Domains hub
  'domains.eyebrow': 'Workstation IDBO · Offre 1', 'domains.title': 'Domaines',
  'domains.intro.lead': 'Outils & ressources spécifiques au domaine, médiés par l’IA',
  'domains.off1.tag': 'Offre 1 · Vous êtes ici', 'domains.off1.title': 'Travaillez maintenant avec les outils de domaine',
  'domains.off2.tag': 'Offre 2', 'domains.off2.title': 'Établir une entreprise vivante',
  'domains.six': 'Les six domaines', 'domains.browseAll': 'Parcourir les', 'domains.tools': 'outils', 'domains.open': 'Ouvrir',
};

const es: Dict = {
  'home.eyebrow': 'Workstation IDBO · Centro de Mando',
  'home.title.concept': 'Concepto',
  'home.title.commercialisation': 'Comercialización',
  'home.welcome': 'Bienvenido',
  'home.intro': 'Mediado por IA, sobre la IA nativa de Workstation.',
  'home.intro.work': 'Trabaja en tu dominio ahora',
  'home.intro.or': 'o',
  'home.intro.build': 'crea una empresa viva',
  'home.intro.tail': 'que se gestiona sola.',
  'home.searchMesh': 'Buscar',
  'home.consultCEO': 'Consultar al CEO',
  'home.journey1.eyebrow': 'Oferta 1 · Trabaja ahora',
  'home.journey1.title': 'Trabajar en un Dominio',
  'home.journey1.cta': 'Abrir Dominios',
  'home.journey2.eyebrow': 'Oferta 2 · Crea una empresa',
  'home.journey2.title': 'Concepto → Comercialización',
  'home.journey2.cta': 'Iniciar un Genesis',
  'home.platform': 'La Plataforma',
  'home.recent': 'Continuar · Trabajo reciente',
  'home.myWork': 'Mi Trabajo',
  'home.organism': 'Organismo Vivo',
  'home.openOrganism': 'Abrir Organismo',
  'navsec.home-facet': 'Inicio', 'navsec.domains-facet': 'Dominios', 'navsec.vsb-facet': 'Empresas VSB',
  'navsec.econ-facet': 'Transformación y Economía', 'navsec.gov-facet': 'Gobernanza y Confianza', 'navsec.dev-facet': 'Desarrollador y Sistema',
  'navsec.work-facet': 'Trabajar en un dominio', 'navsec.build-facet': 'Crear una empresa', 'navsec.platform-facet': 'Plataforma', 'navsec.system-facet': 'Sistema',
  'nav.dashboard': 'Panel', 'nav.my-work': 'Mi Trabajo', 'nav.organism': 'Organismo', 'nav.projects': 'Proyectos',
  'nav.marketplace': 'Mercado', 'nav.wallet': 'Cartera', 'nav.deliverables': 'Entregables', 'nav.compliance': 'Cumplimiento',
  'nav.constitution': 'Constitución', 'nav.settings': 'Ajustes', 'nav.domains': 'Resumen',
  'nav.religion': 'Religión', 'nav.science': 'Ciencia', 'nav.education': 'Educación', 'nav.law': 'Derecho', 'nav.care': 'Cuidado', 'nav.employment': 'Empleo',
  'domains.eyebrow': 'Workstation IDBO · Oferta 1', 'domains.title': 'Dominios',
  'domains.intro.lead': 'Herramientas y recursos específicos del dominio, mediados por IA',
  'domains.off1.tag': 'Oferta 1 · Estás aquí', 'domains.off1.title': 'Trabaja ahora con herramientas de dominio',
  'domains.off2.tag': 'Oferta 2', 'domains.off2.title': 'Establece una empresa viva',
  'domains.six': 'Los seis dominios', 'domains.browseAll': 'Ver las', 'domains.tools': 'herramientas', 'domains.open': 'Abrir',
};

const ur: Dict = {
  'home.eyebrow': 'ورک سٹیشن IDBO · کمانڈ سینٹر',
  'home.title.concept': 'تصور',
  'home.title.commercialisation': 'تجارتی کاری',
  'home.welcome': 'خوش آمدید',
  'home.intro': 'اے آئی کی وساطت سے، ورک سٹیشن کے اپنے مقامی اے آئی پر۔',
  'home.intro.work': 'ابھی اپنے شعبے میں کام کریں',
  'home.intro.or': 'یا',
  'home.intro.build': 'ایک زندہ ادارہ بنائیں',
  'home.intro.tail': 'جو خود کو چلاتا ہے۔',
  'home.searchMesh': 'تلاش کریں',
  'home.consultCEO': 'سی ای او سے مشورہ',
  'home.journey1.eyebrow': 'پیشکش 1 · ابھی کام کریں',
  'home.journey1.title': 'کسی شعبے میں کام کریں',
  'home.journey1.cta': 'شعبے کھولیں',
  'home.journey2.eyebrow': 'پیشکش 2 · ادارہ بنائیں',
  'home.journey2.title': 'تصور ← تجارتی کاری',
  'home.journey2.cta': 'جینیسس شروع کریں',
  'home.platform': 'پلیٹ فارم',
  'home.recent': 'جاری رکھیں · حالیہ کام',
  'home.myWork': 'میرا کام',
  'home.organism': 'زندہ نظام',
  'home.openOrganism': 'نظام کھولیں',
  'navsec.home-facet': 'ہوم', 'navsec.domains-facet': 'شعبے', 'navsec.vsb-facet': 'VSB ادارے',
  'navsec.econ-facet': 'تبدیلی و معیشت', 'navsec.gov-facet': 'گورننس و اعتماد', 'navsec.dev-facet': 'ڈویلپر و سسٹم',
  'navsec.work-facet': 'کسی شعبے میں کام', 'navsec.build-facet': 'ادارہ بنائیں', 'navsec.platform-facet': 'پلیٹ فارم', 'navsec.system-facet': 'سسٹم',
  'nav.dashboard': 'ڈیش بورڈ', 'nav.my-work': 'میرا کام', 'nav.organism': 'زندہ نظام', 'nav.projects': 'منصوبے',
  'nav.marketplace': 'مارکیٹ', 'nav.wallet': 'والٹ', 'nav.deliverables': 'تیار نتائج', 'nav.compliance': 'تعمیل',
  'nav.constitution': 'آئین', 'nav.settings': 'ترتیبات', 'nav.domains': 'جائزہ',
  'nav.religion': 'مذہب', 'nav.science': 'سائنس', 'nav.education': 'تعلیم', 'nav.law': 'قانون', 'nav.care': 'نگہداشت', 'nav.employment': 'روزگار',
  'domains.eyebrow': 'ورک سٹیشن IDBO · پیشکش 1', 'domains.title': 'شعبے',
  'domains.intro.lead': 'شعبہ جاتی، اے آئی کی وساطت سے اوزار و وسائل',
  'domains.off1.tag': 'پیشکش 1 · آپ یہاں ہیں', 'domains.off1.title': 'ابھی شعبہ جاتی اوزار سے کام کریں',
  'domains.off2.tag': 'پیشکش 2', 'domains.off2.title': 'ایک زندہ ادارہ قائم کریں',
  'domains.six': 'چھ شعبے', 'domains.browseAll': 'سب دیکھیں', 'domains.tools': 'اوزار', 'domains.open': 'کھولیں',
};

const DICTS: Record<string, Dict> = { en, ar, fr, es, ur };

export function translate(key: string, lang?: string, fallback?: string): string {
  const base = baseLang(lang ?? getPrefs().language);
  return DICTS[base]?.[key] ?? en[key] ?? fallback ?? key;
}

// Hook: returns t(key, fallback) bound to the current language, and re-renders when the user changes it.
export function useT() {
  const [lang, setLang] = useState<string>(() => getPrefs().language || 'en');
  useEffect(() => {
    const onPrefs = () => setLang(getPrefs().language || 'en');
    window.addEventListener('ws:user-prefs', onPrefs);
    return () => window.removeEventListener('ws:user-prefs', onPrefs);
  }, []);
  const t = useCallback((key: string, fallback?: string) => translate(key, lang, fallback), [lang]);
  return { t, lang, rtl: isRTL(lang) };
}
