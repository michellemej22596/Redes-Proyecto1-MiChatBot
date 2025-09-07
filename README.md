# Genius Notes MCP - Chatbot con Servidores MCP

Un chatbot inteligente que utiliza el protocolo MCP (Model Context Protocol) para procesar archivos, generar contenido educativo y gestionar repositorios de GitHub.

## 🚀 Características Principales

### Servidores MCP Implementados

1. **Filesystem MCP Server** - Procesamiento de archivos
   - Lectura de archivos PDF y Markdown
   - Generación de resúmenes inteligentes
   - Creación de flashcards educativas
   - Procesamiento con IA (OpenAI GPT-3.5-turbo)

2. **Git MCP Server** - Integración con GitHub
   - Creación automática de repositorios
   - Commits automáticos con contenido generado
   - Organización de material de estudio
   - Gestión completa del flujo Git

3. **Genius Notes MCP Server** - Servidor personalizado
   - Flujo completo de procesamiento
   - Integración de todos los servicios
   - API JSON-RPC estándar
   - Logging y monitoreo avanzado

## 🛠️ Tecnologías Utilizadas

- **Frontend**: Next.js 14, React, TypeScript, Tailwind CSS
- **Backend**: Python Flask, JSON-RPC
- **IA**: OpenAI GPT-3.5-turbo
- **Integración**: GitHub API, MCP Protocol
- **UI**: shadcn/ui, Lucide Icons

## 📋 Requisitos Previos

1. **Node.js** (v18 o superior)
2. **Python** (v3.8 o superior)
3. **Cuentas y API Keys**:
   - OpenAI API Key
   - GitHub Personal Access Token

## 🔧 Instalación y Configuración

### 1. Clonar el repositorio
\`\`\`bash
git clone <tu-repositorio>
cd genius-notes-mcp
\`\`\`

### 2. Configurar el frontend (Next.js)
\`\`\`bash
npm install
\`\`\`

### 3. Configurar el backend (Python)
\`\`\`bash
pip install flask flask-cors jsonrpcserver python-dotenv openai PyPDF2 requests
\`\`\`

### 4. Configurar variables de entorno
Copia `.env.example` a `.env` y completa:
\`\`\`env
OPENAI_API_KEY=tu_openai_api_key
GITHUB_TOKEN=tu_github_token
\`\`\`

## 🚀 Ejecución

### 1. Iniciar el servidor MCP
\`\`\`bash
python mcp_servers/my_mcp_server.py
\`\`\`

### 2. Iniciar la aplicación web
\`\`\`bash
npm run dev
\`\`\`

### 3. Probar la integración
\`\`\`bash
python scripts/test_mcp_integration.py
\`\`\`

## 📖 Uso del Sistema

### Escenario Completo Demostrado

El sistema implementa el escenario solicitado:

1. **Procesar un archivo**: Sube un PDF o Markdown
2. **Generar contenido**: El sistema crea resúmenes y flashcards
3. **Crear repositorio**: Se crea automáticamente en GitHub
4. **Realizar commit**: Se sube el README con el contenido procesado

### Comandos del Chatbot

- `"procesar archivo"` - Inicia el procesamiento de documentos
- `"crear repositorio"` - Crea un nuevo repositorio en GitHub
- `"generar resumen"` - Genera resúmenes de contenido
- `"crear flashcards"` - Genera flashcards educativas

## 🔌 API del Servidor MCP

### Endpoints Disponibles

#### `process_document(file_path, options)`
Procesa un archivo y genera contenido educativo.

**Parámetros**:
- `file_path`: Ruta al archivo (.pdf, .md)
- `options`: Configuraciones opcionales

**Respuesta**:
\`\`\`json
{
  "success": true,
  "data": {
    "summary": "Resumen generado...",
    "flashcards": "Flashcards generadas...",
    "processed_at": "2024-01-01T12:00:00"
  }
}
\`\`\`

#### `create_github_repository(repo_name, content, options)`
Crea un repositorio en GitHub con material de estudio.

#### `complete_workflow(file_path, repo_name, options)`
Ejecuta el flujo completo: procesa archivo y crea repositorio.

### Health Check
\`\`\`bash
curl http://localhost:5000/health
\`\`\`

## 🧪 Pruebas

### Prueba Automática
\`\`\`bash
npm run test-mcp
\`\`\`

### Prueba Manual
1. Coloca un archivo PDF o Markdown en el directorio
2. Usa el chatbot para procesarlo
3. Verifica que se cree el repositorio en GitHub

## 📁 Estructura del Proyecto

\`\`\`
genius-notes-mcp/
├── app/                    # Frontend Next.js
│   ├── page.tsx           # Interfaz principal del chatbot
│   ├── layout.tsx         # Layout de la aplicación
│   └── globals.css        # Estilos globales
├── components/            # Componentes UI
├── mcp_servers/          # Servidores MCP
│   ├── filesystem_mcp.py # Procesamiento de archivos
│   ├── git_mcp.py        # Integración GitHub
│   └── my_mcp_server.py  # Servidor principal
├── scripts/              # Scripts de utilidad
│   └── test_mcp_integration.py
└── README.md
\`\`\`

## 🔒 Seguridad

- Las API keys se manejan mediante variables de entorno
- Validación de tipos de archivo soportados
- Logging completo de todas las operaciones
- Manejo robusto de errores

## 🤝 Contribución

1. Fork el proyecto
2. Crea una rama para tu feature
3. Commit tus cambios
4. Push a la rama
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT.

## 🆘 Soporte

Para problemas o preguntas:
1. Revisa los logs en `genius_notes_mcp.log`
2. Verifica que las API keys estén configuradas
3. Usa el endpoint `/health` para verificar el estado del servidor

---

**Desarrollado con ❤️ usando el protocolo MCP**
