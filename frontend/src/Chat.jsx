import { useState, useRef, useEffect, useCallback } from 'react';
import { queryMDM, submitFeedback } from './api/mdmApi';
import {
  ResponsiveContainer,
  BarChart,
  Bar,
  LineChart,
  Line,
  PieChart,
  Pie,
  Cell,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
} from 'recharts';

/* ───────────────────────── Inline SVG Icons ───────────────────────── */

function ChatIcon() {
  return (
    <svg xmlns="http://www.w3.org/2000/svg" className="w-7 h-7" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.8}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
    </svg>
  );
}

function CloseIcon() {
  return (
    <svg xmlns="http://www.w3.org/2000/svg" className="w-7 h-7" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" />
    </svg>
  );
}

function SendIcon() {
  return (
    <svg xmlns="http://www.w3.org/2000/svg" className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M6 12L3.269 3.126A59.768 59.768 0 0121.485 12 59.77 59.77 0 013.27 20.876L5.999 12zm0 0h7.5" />
    </svg>
  );
}

/* ──────────────────────── Typing Dots Indicator ───────────────────── */

function TypingDots() {
  return (
    <div className="flex items-center gap-1 px-4 py-3">
      <span className="w-2 h-2 rounded-full bg-sky-600 dot-1 inline-block" />
      <span className="w-2 h-2 rounded-full bg-sky-600 dot-2 inline-block" />
      <span className="w-2 h-2 rounded-full bg-sky-600 dot-3 inline-block" />
    </div>
  );
}

/* ──────────────────── Streaming Status Indicator ──────────────────── */

const STATE_MESSAGES = {
  thinking: 'Analyzing your question...',
  generating_query: 'Generating search queries...',
  fetching_data: 'Retrieving relevant documents...',
  composing_response: 'Composing your answer...',
};

function StreamingStatus({ states }) {
  return (
    <div className="flex flex-col gap-1 px-4 py-2">
      {states.map((state, i) => (
        <div
          key={i}
          className={`flex items-center gap-2 text-xs animate-fade-in-up ${
            i === states.length - 1 ? 'text-sky-800' : 'text-sky-800/50'
          }`}
        >
          <span className="w-1.5 h-1.5 rounded-full bg-sky-600 inline-block shrink-0" />
          <span>{state.message}</span>
          {i === states.length - 1 && (
            <div className="flex items-center gap-1 ml-1">
              <span className="w-1.5 h-1.5 rounded-full bg-sky-600 dot-1 inline-block" />
              <span className="w-1.5 h-1.5 rounded-full bg-sky-600 dot-2 inline-block" />
              <span className="w-1.5 h-1.5 rounded-full bg-sky-600 dot-3 inline-block" />
            </div>
          )}
        </div>
      ))}
    </div>
  );
}

/* ───────────────────────── Rich Renderers ──────────────────────────── */

function TableRenderer({ table }) {
  if (!table || !table.columns || !table.rows || table.rows.length === 0) return null;
  
  return (
    <div className="my-3">
      <h4 className="text-xs font-semibold text-sky-900 mb-2 uppercase tracking-wider">
        {table.title || 'Results'}
      </h4>
      <div className="overflow-x-auto rounded-lg border border-sky-200 shadow-sm">
        <table className="w-full text-sm text-left">
          <thead className="bg-sky-50 text-sky-900 uppercase text-xs tracking-wider">
            <tr>
              {table.columns.map((col) => (
                <th key={col} className="px-4 py-2.5 font-semibold whitespace-nowrap">
                  {col.replace(/_/g, ' ')}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {table.rows.map((row, ri) => (
              <tr
                key={ri}
                className={`border-t border-sky-100 ${
                  ri % 2 === 0 ? 'bg-white' : 'bg-sky-50/50'
                } hover:bg-sky-50 transition-colors`}
              >
                {table.columns.map((col, ci) => (
                  <td key={ci} className="px-4 py-2 text-sky-950 whitespace-nowrap">
                    {row[col] !== null && row[col] !== undefined ? String(row[col]) : '-'}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

function MetricRenderer({ chart }) {
  if (!chart || !chart.data) return null;
  
  return (
    <div className="my-3 bg-gradient-to-br from-sky-50 to-sky-100/50 rounded-xl p-6 border border-sky-200 shadow-sm">
      <div className="text-center">
        <div className="text-4xl font-bold text-sky-900 mb-2">
          {chart.data.value.toLocaleString()}
        </div>
        <div className="text-sm text-sky-700 font-medium">
          {chart.data.label}
        </div>
      </div>
    </div>
  );
}

function BarChartRenderer({ chart }) {
  if (!chart || !chart.data || !chart.data.labels) return null;
  
  // Support multiple datasets
  const datasets = chart.data.datasets || [];
  const chartData = chart.data.labels.map((label, i) => {
    const point = { name: label };
    datasets.forEach((dataset, idx) => {
      point[`value${idx}`] = dataset.data[i];
    });
    return point;
  });
  
  const colors = ["#3B82F6", "#10B981", "#F59E0B", "#8B5CF6", "#EF4444"];
  
  return (
    <div className="my-3">
      <h4 className="text-xs font-semibold text-sky-900 mb-2 uppercase tracking-wider">
        {chart.title}
      </h4>
      <div className="bg-sky-50/50 rounded-xl p-3 border border-sky-200">
        <ResponsiveContainer width="100%" height={250}>
          <BarChart data={chartData} margin={{ top: 5, right: 20, left: 0, bottom: 5 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
            <XAxis 
              dataKey="name" 
              tick={{ fill: '#6b7280', fontSize: 11 }}
              angle={-45}
              textAnchor="end"
              height={80}
            />
            <YAxis tick={{ fill: '#6b7280', fontSize: 11 }} />
            <Tooltip
              contentStyle={{
                backgroundColor: '#ffffff',
                border: '1px solid #e5e7eb',
                borderRadius: '8px',
                color: '#374151',
                fontSize: '12px',
              }}
            />
            <Legend wrapperStyle={{ fontSize: '12px', color: '#6b7280' }} />
            {datasets.map((dataset, idx) => (
              <Bar
                key={idx}
                dataKey={`value${idx}`}
                fill={dataset.backgroundColor || colors[idx % colors.length]}
                radius={[6, 6, 0, 0]}
                name={dataset.label || `Series ${idx + 1}`}
              />
            ))}
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}

function LineChartRenderer({ chart }) {
  if (!chart || !chart.data || !chart.data.labels) return null;
  
  // Support multiple datasets
  const datasets = chart.data.datasets || [];
  const chartData = chart.data.labels.map((label, i) => {
    const point = { name: label };
    datasets.forEach((dataset, idx) => {
      point[`value${idx}`] = dataset.data[i];
    });
    return point;
  });
  
  const colors = ["#3B82F6", "#10B981", "#F59E0B", "#8B5CF6", "#EF4444"];
  
  return (
    <div className="my-3">
      <h4 className="text-xs font-semibold text-sky-900 mb-2 uppercase tracking-wider">
        {chart.title}
      </h4>
      <div className="bg-sky-50/50 rounded-xl p-3 border border-sky-200">
        <ResponsiveContainer width="100%" height={250}>
          <LineChart data={chartData} margin={{ top: 5, right: 20, left: 0, bottom: 5 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
            <XAxis 
              dataKey="name" 
              tick={{ fill: '#6b7280', fontSize: 11 }}
              angle={-45}
              textAnchor="end"
              height={80}
            />
            <YAxis tick={{ fill: '#6b7280', fontSize: 11 }} />
            <Tooltip
              contentStyle={{
                backgroundColor: '#ffffff',
                border: '1px solid #e5e7eb',
                borderRadius: '8px',
                color: '#374151',
                fontSize: '12px',
              }}
            />
            <Legend wrapperStyle={{ fontSize: '12px', color: '#6b7280' }} />
            {datasets.map((dataset, idx) => (
              <Line
                key={idx}
                type="monotone"
                dataKey={`value${idx}`}
                stroke={dataset.borderColor || colors[idx % colors.length]}
                strokeWidth={2}
                dot={{ fill: dataset.borderColor || colors[idx % colors.length], r: 4 }}
                name={dataset.label || `Series ${idx + 1}`}
              />
            ))}
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}

function PieChartRenderer({ chart }) {
  if (!chart || !chart.data || !chart.data.labels) return null;
  
  const chartData = chart.data.labels.map((label, i) => ({
    name: label,
    value: chart.data.datasets[0].data[i]
  }));
  
  // Use colors from dataset or default palette
  const COLORS = Array.isArray(chart.data.datasets[0].backgroundColor) 
    ? chart.data.datasets[0].backgroundColor 
    : [
        "#3B82F6", "#10B981", "#F59E0B", "#8B5CF6", 
        "#EF4444", "#06B6D4", "#EC4899", "#14B8A6"
      ];
  
  return (
    <div className="my-3">
      <h4 className="text-xs font-semibold text-sky-900 mb-2 uppercase tracking-wider">
        {chart.title}
      </h4>
      <div className="bg-sky-50/50 rounded-xl p-3 border border-sky-200">
        <ResponsiveContainer width="100%" height={280}>
          <PieChart>
            <Pie
              data={chartData}
              cx="50%"
              cy="45%"
              labelLine={false}
              label={({percent}) => `${(percent * 100).toFixed(0)}%`}
              outerRadius={70}
              dataKey="value"
            >
              {chartData.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
              ))}
            </Pie>
            <Tooltip
              contentStyle={{
                backgroundColor: '#ffffff',
                border: '1px solid #e5e7eb',
                borderRadius: '8px',
                color: '#374151',
                fontSize: '11px',
              }}
            />
            <Legend 
              wrapperStyle={{ fontSize: '12px', color: '#6b7280' }}
              iconSize={10}
            />
          </PieChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}

function KPIRenderer({ kpis }) {
  if (!kpis || kpis.length === 0) return null;
  
  return (
    <div className="my-3 grid grid-cols-2 gap-2">
      {kpis.slice(0, 6).map((kpi, i) => (
        <div key={i} className="bg-sky-50/50 rounded-lg p-3 border border-sky-200">
          <div className="text-xs text-sky-700 mb-1">{kpi.label}</div>
          <div className="text-lg font-bold text-sky-900">
            {typeof kpi.value === 'number' ? kpi.value.toLocaleString() : kpi.value}
            {kpi.unit && <span className="text-sm font-normal text-sky-700 ml-1">{kpi.unit}</span>}
          </div>
        </div>
      ))}
    </div>
  );
}

function TableRenderer_Old({ data }) {
  if (!data || !data.headers || !data.rows) return null;
  return (
    <div className="overflow-x-auto rounded-lg border border-sky-200 my-2">
      <table className="w-full text-sm text-left">
        <thead className="bg-sky-50 text-sky-900 uppercase text-xs tracking-wider">
          <tr>
            {data.headers.map((h) => (
              <th key={h} className="px-4 py-2.5 font-semibold">{h}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {data.rows.map((row, ri) => (
            <tr
              key={ri}
              className={`border-t border-sky-100 ${
                ri % 2 === 0 ? 'bg-white' : 'bg-sky-50/50'
              } hover:bg-sky-50 transition-colors`}
            >
              {row.map((cell, ci) => (
                <td key={ci} className="px-4 py-2 text-sky-950">{cell}</td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

function ChartRenderer_Old({ data }) {
  if (!data || !data.chartData) return null;
  return (
    <div className="my-2 bg-sky-50/50 rounded-xl p-3 border border-sky-200">
      <ResponsiveContainer width="100%" height={220}>
        <BarChart data={data.chartData} margin={{ top: 5, right: 20, left: 0, bottom: 5 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
          <XAxis dataKey="name" tick={{ fill: '#6b7280', fontSize: 11 }} />
          <YAxis tick={{ fill: '#6b7280', fontSize: 11 }} />
          <Tooltip
            contentStyle={{
              backgroundColor: '#ffffff',
              border: '1px solid #e5e7eb',
              borderRadius: '8px',
              color: '#374151',
              fontSize: '12px',
            }}
          />
          <Legend wrapperStyle={{ fontSize: '12px', color: '#6b7280' }} />
          <Bar dataKey="value" fill="#0284c7" radius={[6, 6, 0, 0]} name={data.label || 'Value'} />
          {data.secondaryKey && (
            <Bar dataKey={data.secondaryKey} fill="#06b6d4" radius={[6, 6, 0, 0]} name={data.secondaryLabel || 'Secondary'} />
          )}
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}

/* ───────────────────────── Feedback Widget ──────────────────────────── */

function FeedbackWidget({ query, sql_used }) {
  const [status, setStatus] = useState('idle');
  
  const handleFeedback = async (rating) => {
    try {
      setStatus('submitting');
      await submitFeedback({ query, sql_used, rating });
      setStatus('success');
    } catch (e) {
      console.error(e);
      setStatus('error');
    }
  };

  if (!sql_used) return null;
  if (status === 'success') return <div className="text-xs text-sky-600 mt-2 font-medium">Thanks for your feedback!</div>;

  return (
    <div className="mt-4 pt-3 border-t border-sky-100 flex items-center justify-between">
      <span className="text-xs text-sky-700 font-medium">Was this response helpful?</span>
      <div className="flex gap-2">
        <button onClick={() => handleFeedback(1)} disabled={status !== 'idle'} className="p-1 px-2 hover:bg-sky-100 rounded text-sky-700 disabled:opacity-50 transition-colors" title="Good">Helpful</button>
        <button onClick={() => handleFeedback(-1)} disabled={status !== 'idle'} className="p-1 px-2 hover:bg-sky-100 rounded text-sky-700 disabled:opacity-50 transition-colors" title="Bad">Not Helpful</button>
      </div>
    </div>
  );
}

/* ───────────────────────── Message Bubble ──────────────────────────── */

function MessageBubble({ message }) {
  const isUser = message.role === 'user';

  const renderContent = () => {
    // Handle structured response from backend
    if (message.structuredData) {
      const data = message.structuredData;
      const tone = data.metadata?.tone || 'professional';
      
      return (
        <div>
          {/* Summary with tone-based styling */}
          {data.summary && (
            <div className={`mb-3 p-3 rounded-lg ${
              tone === 'urgent' ? 'bg-red-50 border border-red-200' : 
              tone === 'informative' ? 'bg-blue-50 border border-blue-200' : 
              'bg-white'
            }`}>
              <p className="text-sky-950 leading-relaxed">{data.summary}</p>
            </div>
          )}
          
          {/* Insights */}
          {data.insights && data.insights.length > 0 && (
            <div className="mb-3 bg-sky-50 border border-sky-200 rounded-lg p-3">
              <div className="flex items-center gap-2 mb-2">
                <span className="text-sm font-semibold text-sky-900">Key Insights</span>
              </div>
              <ul className="space-y-1.5">
                {data.insights.map((insight, i) => (
                  <li key={i} className="text-xs text-sky-800 flex items-start gap-2">
                    <span className="text-sky-600 mt-0.5">•</span>
                    <span>{insight}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}
          
          {/* KPIs */}
          {data.kpis && data.kpis.length > 0 && (
            <KPIRenderer kpis={data.kpis} />
          )}
          
          {/* Charts */}
          {data.charts && data.charts.map((chart, i) => {
            if (chart.type === 'metric') {
              return <MetricRenderer key={i} chart={chart} />;
            } else if (chart.type === 'line') {
              return <LineChartRenderer key={i} chart={chart} />;
            } else if (chart.type === 'pie') {
              return <PieChartRenderer key={i} chart={chart} />;
            } else {
              return <BarChartRenderer key={i} chart={chart} />;
            }
          })}
          
          {/* Tables */}
          {data.tables && data.tables.map((table, i) => (
            <TableRenderer key={i} table={table} />
          ))}
          
          {/* Metadata */}
          {data.metadata && (
            <div className="mt-3 pt-3 border-t border-sky-200 text-xs text-sky-700">
              <div className="flex items-center gap-3 flex-wrap">
                <span>{data.metadata.row_count} rows</span>
                {data.metadata.truncated && <span className="text-amber-600 font-semibold px-2 py-1 bg-amber-50 rounded">Showing first 5,000 rows. Narrow your time range for complete results.</span>}
              </div>
            </div>
          )}
          
          <FeedbackWidget query={message.userQuery} sql_used={message.sql_used} />
        </div>
      );
    }
    
    // Legacy format handling
    switch (message.type) {
      case 'table':
        return (
          <div>
            {message.content.text && <p className="mb-2 text-gray-700">{message.content.text}</p>}
            <TableRenderer_Old data={message.content} />
          </div>
        );
      case 'chart':
        return (
          <div>
            {message.content.text && <p className="mb-2 text-gray-700">{message.content.text}</p>}
            <ChartRenderer_Old data={message.content} />
          </div>
        );
      default:
        return <p className="whitespace-pre-wrap leading-relaxed">{message.content}</p>;
    }
  }

  return (
    <div className={`flex animate-fade-in-up ${isUser ? 'justify-end' : 'justify-start'}`}>
      <div
        className={`max-w-[85%] rounded-2xl px-4 py-3 text-sm shadow-sm ${
          isUser
            ? 'bg-sky-600 text-white rounded-br-md'
            : 'bg-white border border-sky-200 text-sky-950 rounded-bl-md'
        }`}
      >
        {!isUser && (
          <div className="flex items-center gap-1.5 mb-1.5">
            <span className="w-1.5 h-1.5 rounded-full bg-sky-600" />
            <span className="text-[10px] font-semibold text-sky-800 uppercase tracking-widest">
              ApparentIQ
            </span>
          </div>
        )}
        {renderContent()}
      </div>
    </div>
  );
}

/* ──────────────────────── Main Chat Component ─────────────────────── */

const API_URL = 'http://localhost:8000';

export default function Chat() {
  const [isOpen, setIsOpen] = useState(false);
  const [isClosing, setIsClosing] = useState(false);
  const [messages, setMessages] = useState([
    {
      id: 'welcome',
      role: 'assistant',
      type: 'text',
      content: 'Hello! I\'m ApparentIQ. Ask me anything about your knowledge base.',
      status: 'complete',
    },
  ]);
  const [input, setInput] = useState('');
  const [isStreaming, setIsStreaming] = useState(false);
  const [streamingStates, setStreamingStates] = useState([]);

  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);

  const scrollToBottom = useCallback(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [messages, streamingStates, scrollToBottom]);

  useEffect(() => {
    if (isOpen && inputRef.current) {
      setTimeout(() => inputRef.current.focus(), 300);
    }
  }, [isOpen]);

  const handleToggle = () => {
    if (isOpen) {
      setIsClosing(true);
      setTimeout(() => {
        setIsOpen(false);
        setIsClosing(false);
      }, 200);
    } else {
      setIsOpen(true);
    }
  };

  const streamResponse = async (query) => {
    setIsStreaming(true);
    setStreamingStates([{ state: 'fetching', message: 'Thinking' }]);

    try {
      const data = await queryMDM({ query });

      setMessages(prev => [
        ...prev,
        {
          id: `ai-${Date.now()}`,
          role: 'assistant',
          type: 'structured',
          content: data.summary || 'Query completed successfully',
          structuredData: data,
          sql_used: data.sql_used,
          userQuery: query,
          status: 'complete',
        },
      ]);
    } catch (error) {
      console.error('Fetch error:', error);
      setMessages(prev => [
        ...prev,
        {
          id: `error-${Date.now()}`,
          role: 'assistant',
          type: 'text',
          content: `Error: ${error.message}`,
          status: 'error',
        },
      ]);
    } finally {
      setIsStreaming(false);
      setStreamingStates([]);
    }
  };

  const handleSend = () => {
    const text = input.trim();
    if (!text || isStreaming) return;

    const userMsg = {
      id: `user-${Date.now()}`,
      role: 'user',
      type: 'text',
      content: text,
      status: 'complete',
    };

    setMessages(prev => [...prev, userMsg]);
    setInput('');
    streamResponse(text);
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <>
      {/* ─── Floating Action Button Area ─── */}
      <div className="fixed bottom-6 right-6 z-50 flex flex-col items-end gap-3">
        {/* Chat Panel */}
        {(isOpen || isClosing) && (
          <div
            className={`w-[min(420px,calc(100vw-2rem))] h-[min(600px,calc(100vh-8rem))] flex flex-col rounded-2xl shadow-xl border border-sky-200 bg-sky-50/30 overflow-hidden origin-bottom-right ${
              isClosing ? 'chat-panel-exit' : 'chat-panel-enter'
            }`}
          >
            {/* Header */}
            <div className="flex items-center justify-between px-5 py-4 bg-sky-600 text-white">
              <div className="flex items-center gap-3">
                <div className="w-9 h-9 rounded bg-white flex items-center justify-center p-0.5 overflow-hidden">
                  <img src="/apparent.jpeg" alt="Apparent Energy" className="w-full h-full object-contain" />
                </div>
                <div>
                  <h3 className="text-sm font-bold tracking-wide">ApparentIQ</h3>
                  <p className="text-[10px] text-sky-100 flex items-center gap-1">
                    <span className="w-1.5 h-1.5 rounded-full bg-emerald-300" />
                    Online — Ready to help
                  </p>
                </div>
              </div>
              <button
                onClick={handleToggle}
                className="p-1.5 rounded-lg text-white/70 hover:text-white hover:bg-white/10 transition-all duration-200"
                aria-label="Close chat"
              >
                <CloseIcon />
              </button>
            </div>

            {/* Messages */}
            <div className="flex-1 overflow-y-auto chat-scrollbar p-4 space-y-3 bg-sky-50/40">
              {messages.map((msg) => (
                <MessageBubble key={msg.id} message={msg} />
              ))}

              {/* Streaming Indicator */}
              {isStreaming && (
                <div className="flex justify-start">
                  <div className="max-w-[85%] rounded-2xl rounded-bl-md bg-white border border-sky-200 shadow-sm">
                    {streamingStates.length > 0 ? (
                      <StreamingStatus states={streamingStates} />
                    ) : (
                      <TypingDots />
                    )}
                  </div>
                </div>
              )}

              <div ref={messagesEndRef} />
            </div>

            {/* Input Area */}
            <div className="p-3 border-t border-sky-200 bg-white">
              <div className="flex items-center gap-2 bg-sky-50/50 rounded-xl border border-sky-200 focus-within:border-sky-500 focus-within:ring-1 focus-within:ring-sky-200 transition-all duration-200 px-3 py-1.5">
                <input
                  ref={inputRef}
                  type="text"
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  onKeyDown={handleKeyDown}
                  placeholder="Ask something..."
                  disabled={isStreaming}
                  className="flex-1 bg-transparent text-sm text-sky-950 placeholder-sky-800/40 outline-none py-2 disabled:opacity-50"
                />
                <button
                  onClick={handleSend}
                  disabled={!input.trim() || isStreaming}
                  className="p-2 rounded-lg bg-sky-600 text-white hover:bg-sky-700 disabled:opacity-30 disabled:cursor-not-allowed transition-all duration-200 active:scale-95"
                  aria-label="Send message"
                >
                  <SendIcon />
                </button>
              </div>
              <p className="text-[10px] text-sky-800/40 text-center mt-2">
                Powered by RAG · Responses may be generated from retrieved documents
              </p>
            </div>
          </div>
        )}

        {/* Toggle Button */}
        <button
          onClick={handleToggle}
          className="relative w-14 h-14 rounded-full bg-sky-600 text-white shadow-lg hover:bg-sky-700 hover:scale-110 active:scale-95 transition-all duration-300 flex items-center justify-center group"
          aria-label={isOpen ? 'Close chat' : 'Open chat'}
        >
          {!isOpen && (
            <span className="absolute inset-0 rounded-full bg-sky-500/30 pulse-ring" />
          )}
          <span className="transition-transform duration-300 group-hover:rotate-12">
            {isOpen ? <CloseIcon /> : <ChatIcon />}
          </span>
        </button>
      </div>
    </>
  );
}