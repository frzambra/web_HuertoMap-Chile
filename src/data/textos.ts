// All visible copy for the site (Spanish, es-CL).
// Every number cites its source in clasificacion_huertos; re-check before each release.
// Source of headline numbers: book/index.qmd (state as of 2026-11-23).

export const sitio = {
  nombre: 'HuertoMap-Chile',
  titulo: 'HuertoMap-Chile · Mapas de huertos frutales desde satélite',
  descripcion:
    'Mapas de huertos frutales y su especie a 10 m de resolución para Chile, con imágenes Sentinel-2 y Sentinel-1, aplicables a temporadas nuevas sin reentrenar.',
};

export const nav = [
  { href: '#productos', texto: 'Productos' },
  { href: '#metodo', texto: 'Método' },
  { href: '#exactitud', texto: 'Exactitud' },
  { href: '#cobertura', texto: 'Cobertura' },
  { href: '#mapa', texto: 'Mapa' },
];

export const hero = {
  antetitulo: 'Teledetección para la fruticultura chilena',
  titulo: 'Los huertos frutales de Chile, mapeados cada temporada.',
  bajada:
    'HuertoMap-Chile identifica dónde hay huertos y qué especie se cultiva en cada uno, a 10 m de resolución, con imágenes Sentinel-2 y Sentinel-1. Los modelos se aplican a temporadas nuevas sin reentrenar y sin esperar el próximo catastro.',
  cta1: { href: '#mapa', texto: 'Explorar el mapa' },
  cta2: { href: '#metodo', texto: 'Cómo funciona' },
  pie: 'Especie predicha en Curicó y Molina, Región del Maule. Temporada 2023/24, con modelos que no vieron esa temporada.',
  datos: [
    { valor: '10 m', texto: 'resolución espacial' },
    { valor: '16', texto: 'clases de especie' },
    // Pilots (4) + extension regions (2), source CLAUDE.md.
    { valor: '6', texto: 'regiones validadas' },
    // data/interim/catastro_all.parquet = 293,736 polygons.
    { valor: '293.736', texto: 'huertos de referencia' },
  ],
};

export const productos = {
  antetitulo: 'Productos',
  titulo: 'Tres capas, un mismo mapa.',
  bajada:
    'El sistema trabaja en dos etapas: primero decide si un píxel es huerto y, solo donde lo es, asigna la especie.',
  items: [
    {
      nombre: 'Huerto / no huerto',
      texto:
        'La superficie frutal, píxel a píxel, separada de cultivos anuales, praderas, bosque y zonas urbanas. Mapa limpio con unidad mínima de 0,5 ha.',
      dato: 'F1 0,96',
    },
    {
      nombre: 'Especie',
      texto:
        'Quince especies y un grupo de otras: cerezo, manzano, arándano, nogal, avellano, uva de mesa, palto, cítricos, kiwi y más.',
      dato: 'macro-F1 0,87',
    },
    {
      nombre: 'Cerezo',
      texto:
        'Un modelo dedicado a la principal especie de exportación, con decisión por huerto completo y no solo por píxel.',
      dato: 'F1 por huerto 0,92',
    },
  ],
  notaDatos: 'Exactitud en la temporada del catastro, cuatro regiones piloto.',
};

export const metodo = {
  antetitulo: 'Método',
  titulo: 'De la órbita al huerto.',
  pasos: [
    {
      titulo: 'Imágenes',
      texto:
        'Sentinel-2 óptico, con nubes enmascaradas mediante Cloud Score+, y Sentinel-1 radar, que observa a través de las nubes. Toda la temporada agrícola, de julio a junio.',
      detalle: 'Sentinel-2 L2A · Sentinel-1 VV/VH',
    },
    {
      titulo: 'Variables',
      texto:
        'Índices de vegetación mensuales, armónicos que resumen la fenología y retrodispersión radar. Cada píxel queda descrito por su ciclo anual.',
      detalle: '236 variables por píxel',
    },
    {
      titulo: 'Modelos',
      texto:
        'Gradient boosting entrenado con el Catastro Frutícola. La validación separa huertos completos, regiones y temporadas, nunca píxeles sueltos.',
      detalle: 'LightGBM · validación espacial y temporal',
    },
    {
      titulo: 'Mapa',
      texto:
        'Umbral ajustado a la superficie esperada según la tendencia de los catastros, limpieza morfológica y unidad mínima de 0,5 ha.',
      detalle: 'GeoTIFF optimizado para la nube',
    },
  ],
  destacado: {
    titulo: 'Probado en temporadas que el modelo no conoce',
    texto:
      'Los modelos se entrenan con catastros pasados y se aplican tal cual, umbrales incluidos, a una temporada sin etiquetas. Esa es la prueba principal de exactitud: la misma situación en que se usará el mapa.',
  },
};

// book/index.qmd, "Resultados".
export const exactitud = {
  antetitulo: 'Exactitud',
  titulo: 'Cifras medidas contra el catastro oficial.',
  bajada:
    'Dos escenarios: la temporada del catastro, con validación espacial, y una temporada completa que el modelo nunca vio.',
  filas: [
    { capa: 'Huerto / no huerto', metrica: 'F1', misma: '0,96', nueva: '0,93–0,97' },
    { capa: 'Especie', metrica: 'macro-F1', misma: '0,87', nueva: '0,58–0,75' },
    { capa: 'Cerezo', metrica: 'F1 por huerto', misma: '0,92', nueva: '0,72–0,90' },
  ],
  cabeceras: { capa: 'Capa', misma: 'Temporada del catastro', nueva: 'Temporada no vista' },
  destacadas: [
    { valor: '95–99 %', texto: 'de los huertos del catastro detectados en una temporada no vista' },
    { valor: '1,01×', texto: 'superficie frutal del mapa respecto al catastro, Maule 2023/24' },
    { valor: '1,00–1,02×', texto: 'superficie de cerezo respecto al catastro en los mapas continuos' },
  ],
  limitaciones: [
    'El catastro no registra viñas para vino, así que parte del exceso del mapa son huertos o viñas ausentes del catastro y no necesariamente errores.',
    'Las métricas provienen de muestras y no estiman aún la exactitud por superficie. Una validación independiente con muestreo probabilístico está prevista para 2027.',
    'El modelo huerto / no huerto es más débil en Coquimbo.',
  ],
};

// Regions north to south. Catastro years and map seasons from the source CLAUDE.md.
export const cobertura = {
  antetitulo: 'Cobertura',
  titulo: 'De Coquimbo a La Araucanía.',
  bajada:
    'Ocho regiones con catastros o mapas. Los modelos de especie se entrenan con regiones combinadas para extenderse a toda la zona frutícola del país.',
  leyenda: { piloto: 'Región piloto', extension: 'Extensión', mapa: 'Validación de mapa' },
  regiones: [
    { nombre: 'Coquimbo', rol: 'piloto', catastros: '2021 · 2024', mapa: false },
    { nombre: 'Valparaíso', rol: 'mapa', catastros: '2025', mapa: true },
    { nombre: 'Metropolitana', rol: 'mapa', catastros: '2025', mapa: true },
    { nombre: "O'Higgins", rol: 'piloto', catastros: '2021 · 2024', mapa: true },
    { nombre: 'Maule', rol: 'piloto', catastros: '2022 · 2024', mapa: true },
    { nombre: 'Ñuble', rol: 'extension', catastros: '2022 · 2025', mapa: true },
    { nombre: 'Biobío', rol: 'extension', catastros: '2021 · 2024', mapa: false },
    { nombre: 'La Araucanía', rol: 'piloto', catastros: '2021 · 2024', mapa: false },
  ],
  cabeceras: { region: 'Región', rol: 'Rol', catastros: 'Catastros usados', mapa: 'Mapa 2025/26' },
  hitos: [
    { fecha: 'Diciembre 2026', texto: 'Mapas de la temporada 2025/26 para Valparaíso, Metropolitana, O’Higgins, Maule y Ñuble.' },
    { fecha: '2027', texto: 'Validación independiente con muestreo probabilístico.' },
  ],
};

export const mapa = {
  antetitulo: 'Mapa',
  titulo: 'Compare con el catastro.',
  bajada:
    'Curicó y Molina, Región del Maule, temporada 2023/24. A la izquierda, el Catastro Frutícola 2024; a la derecha, el mapa hecho con modelos que no vieron esa temporada ni su catastro. Arrastre el divisor para comparar.',
  // Short part always visible; the rest only from 640 px up.
  rotulos: {
    catastro: { corto: 'Catastro', resto: '2024' },
    prediccion: { corto: 'Predicción', resto: 'HuertoMap' },
  },
  divisor: 'Divisor entre catastro y predicción',
  capas: { especies: 'Especie', huerto: 'Huerto' },
  opacidad: 'Opacidad',
  cargando: 'Cargando mapa…',
  ayuda: 'Arrastre el mapa para moverlo; use + y − o Ctrl + rueda para acercar. El divisor también se mueve con las flechas del teclado.',
  // scripts/tiles.py prints this ratio for the crop.
  nota: 'En este recorte, la superficie frutal mapeada es 1,16 veces la del catastro. Parte de la diferencia corresponde a viñas para vino y huertos que el catastro no registra.',
  fondo: 'Fondo: Sentinel-2 cloudless 2020 de EOX.',
};

export const usos = {
  antetitulo: 'Aplicaciones',
  titulo: 'Para quién es.',
  items: [
    { titulo: 'Política sectorial', texto: 'Superficie frutal por comuna y especie entre catastros, para planificar y focalizar instrumentos.' },
    { titulo: 'Exportación', texto: 'Seguimiento anual de la superficie de cerezo y otras especies de exportación.' },
    { titulo: 'Agua y territorio', texto: 'Demanda hídrica de los huertos, cambios de uso de suelo y expansión frutícola.' },
    { titulo: 'Investigación', texto: 'Una base espacial coherente entre temporadas para estudios de clima, fenología y agronomía.' },
  ],
};

// TODO(usuario): reemplazar con la institución, el equipo y el correo reales.
export const contacto = {
  antetitulo: 'Contacto',
  titulo: '¿Le interesa usar los mapas?',
  texto:
    'Escríbanos para conocer el avance del proyecto, solicitar una región o colaborar en la validación.',
  correo: 'contacto@ejemplo.cl', // TODO(usuario)
  institucion: '[Nombre de la institución]', // TODO(usuario)
  equipo: [
    { nombre: '[Nombre]', rol: '[Rol]' }, // TODO(usuario)
  ],
};

export const pie = {
  creditos: [
    'Contiene datos modificados de Copernicus Sentinel.',
    'Datos de referencia: Catastro Frutícola, CIREN.',
    'Mapa base: Sentinel-2 cloudless de EOX (CC BY-NC-SA 4.0).',
  ],
};
