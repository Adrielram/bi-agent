## OBSERVACIONES
# Las tools actuales pasan el archivo entero al llm. Deberia pasar unas lineas
# El agente deberia poder buscar POR PALABRA/s o regex, y traer varias lineas donde este el match, por contexto.
# El agente deberia poder usar tools para por ejemplo usar grep o herramientas que le permitan MANIPULAR el texto extraido antes de pasarlo al llm (para ahorrar tokens y mejorar precision).


## IDEAS A FUTURO
- PREPROCESAMIENTO: en cada cambio de empresa_docs, crear una guia de la informacion. Podria ser un .md. En cada conversacion, se chequea si existe el .md que tenga un nombre estandarizado, y si no existe se crea. Sirve para que el agente se ahorre EN CADA NUEVO CHAT analizar los datos para saber QUE esta en donde. En otras palabras, sirve como un indice para el agente.

- agentes: 1, 3, 5, 6
  - Agente de Monitoreo: Detecta problemas de latencia, errores y métricas
    Ej: Detecta que la latencia subió de 2.5s a 4.2s y genera alerta
  - Agente de Seguridad: Validación de inputs/outputs, protección contra inyecciones
    Ej: Detecta intento de "prompt injection" y bloquea la consulta
  - Agente de Datos: Valida esquemas JSON y detecta inconsistencias (podria ser parte del preprocesamiento de empresa_docs !!)
    Ej: Encuentra que en consultores.json hay campos faltantes o malformados
  - Agente de LangGraph: Optimiza el rendimiento del grafo de ejecución
    Ej: Detecta que una consulta simple hace 3 llamadas innecesarias a herramientas
