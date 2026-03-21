import Chat from './Chat';

function App() {
  return (
    <div className="min-h-screen bg-sky-50 text-sky-950">
      {/* ─── Demo Landing Content (replace with your actual app) ─── */}
      <div className="flex flex-col items-center justify-center min-h-screen px-6 text-center">
        <div className="mb-8">
          <img src="/apparent.jpeg" alt="Apparent Energy" className="mx-auto h-24 mb-4 drop-shadow-sm rounded-lg object-contain bg-white p-2" />
        </div>

        <h1 className="text-4xl md:text-5xl font-extrabold tracking-tight mb-4 text-sky-900">
          Apparent Energy Dashboard
        </h1>

        <p className="text-sky-800/60 max-w-md text-lg leading-relaxed mb-8">
          Ask questions about your documents using the AI-powered chat assistant.
        </p>

        <div className="flex items-center gap-2 text-sm text-sky-800/50">
          <span className="w-2 h-2 rounded-full bg-emerald-600" />
          Click the chat button to get started
          <svg xmlns="http://www.w3.org/2000/svg" className="w-4 h-4 animate-bounce" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
            <path strokeLinecap="round" strokeLinejoin="round" d="M17 8l4 4m0 0l-4 4m4-4H3" />
          </svg>
        </div>
      </div>

      {/* ─── Chat Widget ─── */}
      <Chat />
    </div>
  );
}

export default App;
