# Las tools actuales pasan el archivo entero al llm. Deberia pasar unas lineas
# El agente deberia poder buscar POR PALABRA/s o regex, y traer varias lineas donde este el match, por contexto. 
# El agente deberia poder usar tools para por ejemplo usar grep o herramientas que le permitan MANIPULAR el texto extraido antes de pasarlo al llm (para ahorrar tokens y mejorar precision). 