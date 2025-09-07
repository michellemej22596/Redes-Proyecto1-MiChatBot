"use client"

import type React from "react"

import { useState, useRef, useEffect } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Separator } from "@/components/ui/separator"
import { ScrollArea } from "@/components/ui/scroll-area"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Send, FileText, GitBranch, Brain, Upload, Github, Folder, Sparkles } from "lucide-react"

interface Message {
  id: string
  type: "user" | "assistant" | "system"
  content: string
  timestamp: Date
  mcpAction?: {
    type: "filesystem" | "git" | "genius-notes"
    data: any
  }
}

interface MCPResult {
  type: "summary" | "flashcards" | "repo-created" | "file-processed"
  content: string
  metadata?: any
}

export default function ChatbotPage() {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: "1",
      type: "system",
      content:
        "¡Hola! Soy Genius Notes, tu asistente MCP. Puedo ayudarte con:\n\n• 📁 Procesar archivos PDF y Markdown\n• 🧠 Generar resúmenes y flashcards\n• 🔗 Crear repositorios en GitHub\n• ✨ Gestionar tus notas y tareas\n\n¿En qué puedo ayudarte hoy?",
      timestamp: new Date(),
    },
  ])
  const [input, setInput] = useState("")
  const [isLoading, setIsLoading] = useState(false)
  const [mcpStatus, setMcpStatus] = useState({
    filesystem: "connected",
    git: "connected",
    geniusNotes: "connected",
  })
  const messagesEndRef = useRef<HTMLDivElement>(null)
  const fileInputRef = useRef<HTMLInputElement>(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const handleSendMessage = async () => {
    if (!input.trim()) return

    const userMessage: Message = {
      id: Date.now().toString(),
      type: "user",
      content: input,
      timestamp: new Date(),
    }

    setMessages((prev) => [...prev, userMessage])
    setInput("")
    setIsLoading(true)

    // Simular procesamiento MCP
    setTimeout(() => {
      const response = processUserInput(input)
      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        type: "assistant",
        content: response.content,
        timestamp: new Date(),
        mcpAction: response.mcpAction,
      }

      setMessages((prev) => [...prev, assistantMessage])
      setIsLoading(false)
    }, 1500)
  }

  const processUserInput = (input: string) => {
    const lowerInput = input.toLowerCase()

    if (lowerInput.includes("repositorio") || lowerInput.includes("github") || lowerInput.includes("repo")) {
      return {
        content:
          "🔗 Perfecto! Voy a crear un repositorio en GitHub para ti. Necesito el nombre del repositorio y una descripción breve.",
        mcpAction: {
          type: "git" as const,
          data: { action: "create_repo", status: "pending" },
        },
      }
    }

    if (lowerInput.includes("archivo") || lowerInput.includes("pdf") || lowerInput.includes("markdown")) {
      return {
        content:
          "📁 Excelente! Puedo procesar tu archivo PDF o Markdown para generar resúmenes y flashcards. Por favor, sube el archivo usando el botón de adjuntar.",
        mcpAction: {
          type: "filesystem" as const,
          data: { action: "process_file", status: "ready" },
        },
      }
    }

    if (lowerInput.includes("resumen") || lowerInput.includes("flashcard")) {
      return {
        content:
          "🧠 ¡Genial! Puedo crear resúmenes inteligentes y flashcards de cualquier contenido. Comparte el texto o sube un archivo para comenzar.",
        mcpAction: {
          type: "genius-notes" as const,
          data: { action: "generate_content", status: "ready" },
        },
      }
    }

    return {
      content:
        "✨ Entiendo tu solicitud. Como asistente MCP, puedo ayudarte con procesamiento de archivos, gestión de repositorios Git, y generación de contenido educativo. ¿Podrías ser más específico sobre lo que necesitas?",
    }
  }

  const handleFileUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0]
    if (!file) return

    const fileMessage: Message = {
      id: Date.now().toString(),
      type: "user",
      content: `📎 Archivo subido: ${file.name} (${(file.size / 1024).toFixed(1)} KB)`,
      timestamp: new Date(),
    }

    setMessages((prev) => [...prev, fileMessage])

    // Simular procesamiento del archivo
    setTimeout(() => {
      const response: Message = {
        id: (Date.now() + 1).toString(),
        type: "assistant",
        content: `✅ Archivo procesado exitosamente!\n\n📋 **Resumen generado:**\nEl documento contiene información relevante sobre el tema solicitado...\n\n🎯 **Flashcards creadas:**\n• Pregunta 1: ¿Cuál es el concepto principal?\n• Pregunta 2: ¿Cómo se aplica en la práctica?\n• Pregunta 3: ¿Cuáles son los beneficios?`,
        timestamp: new Date(),
        mcpAction: {
          type: "filesystem",
          data: {
            action: "file_processed",
            filename: file.name,
            summary: "Resumen generado",
            flashcards: 3,
          },
        },
      }
      setMessages((prev) => [...prev, response])
    }, 2000)
  }

  const MCPStatusIndicator = ({ type, status }: { type: string; status: string }) => (
    <div className="flex items-center gap-2">
      <div className={`w-2 h-2 rounded-full ${status === "connected" ? "bg-green-500" : "bg-red-500"}`} />
      <span className="text-sm text-muted-foreground">{type}</span>
    </div>
  )

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900">
      <div className="container mx-auto p-4 h-screen flex flex-col">
        {/* Header */}
        <Card className="mb-4 border-2 border-blue-200 dark:border-blue-800">
          <CardHeader className="pb-3">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                <div className="p-2 bg-gradient-to-r from-blue-500 to-purple-600 rounded-lg">
                  <Brain className="h-6 w-6 text-white" />
                </div>
                <div>
                  <CardTitle className="text-xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                    Genius Notes MCP
                  </CardTitle>
                  <p className="text-sm text-muted-foreground">Asistente inteligente con servidores MCP</p>
                </div>
              </div>
              <div className="flex gap-4">
                <MCPStatusIndicator type="Filesystem" status={mcpStatus.filesystem} />
                <MCPStatusIndicator type="Git" status={mcpStatus.git} />
                <MCPStatusIndicator type="Genius Notes" status={mcpStatus.geniusNotes} />
              </div>
            </div>
          </CardHeader>
        </Card>

        {/* Main Content */}
        <div className="flex-1 flex gap-4">
          {/* Chat Area */}
          <Card className="flex-1 flex flex-col">
            <CardContent className="flex-1 flex flex-col p-0">
              <ScrollArea className="flex-1 p-4">
                <div className="space-y-4">
                  {messages.map((message) => (
                    <div
                      key={message.id}
                      className={`flex ${message.type === "user" ? "justify-end" : "justify-start"}`}
                    >
                      <div
                        className={`max-w-[80%] rounded-lg p-3 ${
                          message.type === "user"
                            ? "bg-blue-500 text-white"
                            : message.type === "system"
                              ? "bg-gradient-to-r from-purple-100 to-blue-100 dark:from-purple-900 dark:to-blue-900 border-2 border-purple-200 dark:border-purple-700"
                              : "bg-muted"
                        }`}
                      >
                        <div className="whitespace-pre-wrap text-sm">{message.content}</div>
                        {message.mcpAction && (
                          <div className="mt-2 pt-2 border-t border-white/20">
                            <Badge variant="secondary" className="text-xs">
                              MCP: {message.mcpAction.type}
                            </Badge>
                          </div>
                        )}
                        <div className="text-xs opacity-70 mt-1">{message.timestamp.toLocaleTimeString()}</div>
                      </div>
                    </div>
                  ))}
                  {isLoading && (
                    <div className="flex justify-start">
                      <div className="bg-muted rounded-lg p-3">
                        <div className="flex items-center gap-2">
                          <Sparkles className="h-4 w-4 animate-spin" />
                          <span className="text-sm">Procesando con MCP...</span>
                        </div>
                      </div>
                    </div>
                  )}
                </div>
                <div ref={messagesEndRef} />
              </ScrollArea>

              <Separator />

              {/* Input Area */}
              <div className="p-4">
                <div className="flex gap-2">
                  <Button
                    variant="outline"
                    size="icon"
                    onClick={() => fileInputRef.current?.click()}
                    className="shrink-0"
                  >
                    <Upload className="h-4 w-4" />
                  </Button>
                  <Input
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    placeholder="Escribe tu mensaje aquí..."
                    onKeyPress={(e) => e.key === "Enter" && handleSendMessage()}
                    className="flex-1"
                  />
                  <Button onClick={handleSendMessage} disabled={isLoading}>
                    <Send className="h-4 w-4" />
                  </Button>
                </div>
                <input
                  ref={fileInputRef}
                  type="file"
                  accept=".pdf,.md,.txt"
                  onChange={handleFileUpload}
                  className="hidden"
                />
              </div>
            </CardContent>
          </Card>

          {/* Sidebar */}
          <Card className="w-80">
            <CardHeader>
              <CardTitle className="text-lg">Capacidades MCP</CardTitle>
            </CardHeader>
            <CardContent>
              <Tabs defaultValue="servers" className="w-full">
                <TabsList className="grid w-full grid-cols-2">
                  <TabsTrigger value="servers">Servidores</TabsTrigger>
                  <TabsTrigger value="actions">Acciones</TabsTrigger>
                </TabsList>

                <TabsContent value="servers" className="space-y-3">
                  <div className="space-y-3">
                    <div className="p-3 border rounded-lg">
                      <div className="flex items-center gap-2 mb-2">
                        <Folder className="h-4 w-4 text-blue-500" />
                        <span className="font-medium">Filesystem MCP</span>
                      </div>
                      <p className="text-xs text-muted-foreground">
                        Procesa archivos PDF y Markdown para generar resúmenes y flashcards
                      </p>
                    </div>

                    <div className="p-3 border rounded-lg">
                      <div className="flex items-center gap-2 mb-2">
                        <GitBranch className="h-4 w-4 text-green-500" />
                        <span className="font-medium">Git MCP</span>
                      </div>
                      <p className="text-xs text-muted-foreground">
                        Crea repositorios en GitHub y realiza commits automáticos
                      </p>
                    </div>

                    <div className="p-3 border rounded-lg">
                      <div className="flex items-center gap-2 mb-2">
                        <Brain className="h-4 w-4 text-purple-500" />
                        <span className="font-medium">Genius Notes</span>
                      </div>
                      <p className="text-xs text-muted-foreground">
                        Servidor personalizado para gestión inteligente de notas
                      </p>
                    </div>
                  </div>
                </TabsContent>

                <TabsContent value="actions" className="space-y-3">
                  <div className="space-y-2">
                    <Button variant="outline" size="sm" className="w-full justify-start bg-transparent">
                      <FileText className="h-4 w-4 mr-2" />
                      Procesar archivo
                    </Button>
                    <Button variant="outline" size="sm" className="w-full justify-start bg-transparent">
                      <Github className="h-4 w-4 mr-2" />
                      Crear repositorio
                    </Button>
                    <Button variant="outline" size="sm" className="w-full justify-start bg-transparent">
                      <Brain className="h-4 w-4 mr-2" />
                      Generar resumen
                    </Button>
                    <Button variant="outline" size="sm" className="w-full justify-start bg-transparent">
                      <Sparkles className="h-4 w-4 mr-2" />
                      Crear flashcards
                    </Button>
                  </div>
                </TabsContent>
              </Tabs>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  )
}
