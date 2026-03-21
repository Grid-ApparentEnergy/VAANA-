import Chat from './Chat';

function App() {
  return (
    <div className="min-h-screen bg-sky-50 text-sky-950">
      {/* ─── Demo Landing Content (replace with your actual app) ─── */}
      <div className="flex flex-col items-center justify-center min-h-screen px-6 text-center">
        <div className="mb-8">
          <div className="w-20 h-20 rounded-2xl bg-sky-600 flex items-center justify-center shadow-lg">
            <svg xmlns="http://www.w3.org/2000/svg" className="w-10 h-10 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M9.813 15.904L9 18.75l-.813-2.846a4.5 4.5 0 00-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 003.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 003.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 00-3.09 3.09zM18.259 8.715L18 9.75l-.259-1.035a3.375 3.375 0 00-2.455-2.456L14.25 6l1.036-.259a3.375 3.375 0 002.455-2.456L18 2.25l.259 1.035a3.375 3.375 0 002.455 2.456L21.75 6l-1.036.259a3.375 3.375 0 00-2.455 2.456z" />
            </svg>
          </div>
        </div>

        <h1 className="text-4xl md:text-5xl font-extrabold tracking-tight mb-4 text-sky-900">
          RAG Knowledge Base
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
