#!/usr/bin/env python3
"""
Client MCP simple pour tester le serveur
"""
import asyncio
import json
import sys
from typing import Any, Dict

class MCPClient:
    def __init__(self, server_command: list[str]):
        self.server_command = server_command
        self.process = None
        
    async def start_server(self):
        """Lance le serveur MCP en subprocess"""
        self.process = await asyncio.create_subprocess_exec(
            *self.server_command,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        print(f"✅ Serveur MCP lancé (PID: {self.process.pid})")
        
    async def send_request(self, method: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """Envoie une requête JSON-RPC au serveur"""
        if not self.process:
            raise RuntimeError("Serveur non lancé")
            
        request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": method,
            "params": params or {}
        }
        
        request_json = json.dumps(request) + "\n"
        self.process.stdin.write(request_json.encode())
        await self.process.stdin.drain()
        
        # Lire la réponse
        response_line = await self.process.stdout.readline()
        if not response_line:
            raise RuntimeError("Pas de réponse du serveur")
            
        response = json.loads(response_line.decode())
        return response
        
    async def initialize(self):
        """Initialise la connexion MCP"""
        response = await self.send_request("initialize", {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {
                "name": "simple-mcp-client",
                "version": "1.0.0"
            }
        })
        print("🔗 Connexion initialisée:", response.get("result", {}).get("serverInfo", {}))
        
        # Envoie initialized
        notification = {
            "jsonrpc": "2.0",
            "method": "notifications/initialized"
        }
        notification_json = json.dumps(notification) + "\n"
        self.process.stdin.write(notification_json.encode())
        await self.process.stdin.drain()
        
    async def list_tools(self):
        """Liste les outils disponibles"""
        response = await self.send_request("tools/list")
        tools = response.get("result", {}).get("tools", [])
        print(f"\n🛠️  Outils disponibles ({len(tools)}):")
        for tool in tools:
            print(f"  - {tool['name']}: {tool.get('description', 'Pas de description')}")
        return tools
        
    async def call_tool(self, tool_name: str, arguments: Dict[str, Any]):
        """Appelle un outil"""
        response = await self.send_request("tools/call", {
            "name": tool_name,
            "arguments": arguments
        })
        
        if "error" in response:
            print(f"❌ Erreur: {response['error']}")
            return None
            
        result = response.get("result", {})
        
        # Extraire le contenu selon le format MCP
        if "content" in result and result["content"]:
            content = result["content"][0]
            if "text" in content:
                print(f"✅ Résultat de {tool_name}: {content['text']}")
                return content["text"]
        
        print(f"✅ Résultat de {tool_name}: {result}")
        return result
        
    async def stop_server(self):
        """Arrête le serveur"""
        if self.process:
            self.process.terminate()
            await self.process.wait()
            print("🛑 Serveur arrêté")

async def main():
    """Fonction principale du client"""
    print("🚀 Démarrage du client MCP...")
    
    # Configuration du serveur à lancer
    server_command = [sys.executable, "server_tools.py"]
    
    client = MCPClient(server_command)
    
    try:
        # Démarrer le serveur
        await client.start_server()
        await asyncio.sleep(0.5)  # Attendre que le serveur soit prêt
        
        # Initialiser la connexion
        await client.initialize()
        
        # Lister les outils
        tools = await client.list_tools()
        
        # Tester l'outil add
        if tools:
            print("\n🧪 Test de l'outil 'add':")
            await client.call_tool("add", {"a": 5, "b": 3})
            await client.call_tool("add", {"a": 10, "b": 7})
            
        # Mode interactif
        print("\n💬 Mode interactif (tapez 'quit' pour quitter):")
        while True:
            try:
                user_input = input("\n> Entrez deux nombres (ex: 5 3): ").strip()
                if user_input.lower() in ['quit', 'exit', 'q']:
                    break
                    
                parts = user_input.split()
                if len(parts) == 2:
                    try:
                        a, b = int(parts[0]), int(parts[1])
                        await client.call_tool("add", {"a": a, "b": b})
                    except ValueError:
                        print("❌ Veuillez entrer deux nombres entiers")
                else:
                    print("❌ Format: <nombre1> <nombre2>")
                    
            except KeyboardInterrupt:
                break
                
    except Exception as e:
        print(f"❌ Erreur: {e}")
        
    finally:
        await client.stop_server()

if __name__ == "__main__":
    asyncio.run(main())
