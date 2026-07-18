import app from "./src/app.js";

const PORT = process.env.PORT || 3000;

const server = app.listen(PORT, () => {
  console.log(`🚀 Server is running at http://localhost:${PORT}`);
});

server.on("error", (error) => {
  console.error("❌ Failed to start server:", error.message);
  process.exit(1);
});

process.on("SIGINT", () => {
  console.log("\n🛑 Shutting down server...");
  server.close(() => {
    console.log("✅ Server closed.");
    process.exit(0);
  });
});