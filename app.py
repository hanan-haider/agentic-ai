import React, { useState } from 'react';
import { FileText, HelpCircle, CheckCircle, Copy, RefreshCw } from 'lucide-react';

const AssignmentQuizGenerator = () => {
  const [inputText, setInputText] = useState('');
  const [topic, setTopic] = useState('');
  const [inputMode, setInputMode] = useState('text');
  const [assignments, setAssignments] = useState([]);
  const [quizzes, setQuizzes] = useState([]);
  const [generated, setGenerated] = useState(false);
  const [copied, setCopied] = useState(false);

  const extractKeywords = (text) => {
    const words = text.toLowerCase()
      .replace(/[.,!?;:()]/g, '')
      .split(/\s+/)
      .filter(word => word.length > 4);
    
    const commonWords = ['about', 'there', 'their', 'which', 'would', 'could', 'should', 'these', 'those'];
    return words.filter(word => !commonWords.includes(word)).slice(0, 10);
  };

  const extractSentences = (text) => {
    return text.match(/[^.!?]+[.!?]+/g) || [text];
  };

  const generateAssignments = (text, keywords) => {
    const sentences = extractSentences(text);
    const assignments = [];

    if (keywords.length > 0) {
      assignments.push({
        question: `Write an essay analyzing the key concepts of ${keywords.slice(0, 3).join(', ')} as discussed in the provided material. Include specific examples and explanations.`,
        type: 'Essay'
      });
    }

    if (sentences.length > 2) {
      assignments.push({
        question: `Based on the material provided, discuss the main ideas and their implications. Provide a critical analysis with supporting arguments.`,
        type: 'Analysis'
      });
    }

    return assignments;
  };

  const generateTopicAssignments = (topic) => {
    return [
      {
        question: `Write a comprehensive essay on "${topic}". Discuss its key aspects, historical context, and current relevance.`,
        type: 'Essay'
      },
      {
        question: `Analyze the impact and significance of ${topic}. Include real-world examples and potential future developments.`,
        type: 'Analysis'
      }
    ];
  };

  const generateQuizzes = (text, keywords, sentences) => {
    const quizzes = [];
    
    if (keywords.length >= 3) {
      quizzes.push({
        question: `Which of the following is a key concept discussed in the material?`,
        options: [
          keywords[0].charAt(0).toUpperCase() + keywords[0].slice(1),
          'Random concept A',
          'Random concept B',
          'Random concept C'
        ],
        answer: 0
      });
    }

    if (sentences.length > 0) {
      const sentence = sentences[0].trim();
      quizzes.push({
        question: `According to the material, which statement is most accurate?`,
        options: [
          sentence.length > 80 ? sentence.substring(0, 80) + '...' : sentence,
          'This is an incorrect statement',
          'This is also incorrect',
          'Another wrong option'
        ],
        answer: 0
      });
    }

    if (keywords.length >= 2) {
      quizzes.push({
        question: `What is the relationship between the concepts discussed?`,
        options: [
          'They are interconnected and build upon each other',
          'They are completely unrelated',
          'Only one is mentioned in the text',
          'They contradict each other'
        ],
        answer: 0
      });
    }

    return quizzes;
  };

  const generateTopicQuizzes = (topic) => {
    return [
      {
        question: `What is ${topic} primarily concerned with?`,
        options: [
          'Core concepts and principles related to the topic',
          'Unrelated subject matter',
          'Only historical facts',
          'None of the above'
        ],
        answer: 0
      },
      {
        question: `Which approach is most relevant when studying ${topic}?`,
        options: [
          'A comprehensive analytical approach',
          'Ignoring all context',
          'Only memorizing facts',
          'Avoiding critical thinking'
        ],
        answer: 0
      },
      {
        question: `Why is understanding ${topic} important?`,
        options: [
          'It provides valuable insights and practical applications',
          'It has no real-world relevance',
          'It is only for entertainment',
          'It should be ignored'
        ],
        answer: 0
      }
    ];
  };

  const handleGenerate = () => {
    if (inputMode === 'text' && inputText.trim()) {
      const keywords = extractKeywords(inputText);
      const sentences = extractSentences(inputText);
      
      setAssignments(generateAssignments(inputText, keywords));
      setQuizzes(generateQuizzes(inputText, keywords, sentences));
      setGenerated(true);
    } else if (inputMode === 'topic' && topic.trim()) {
      setAssignments(generateTopicAssignments(topic));
      setQuizzes(generateTopicQuizzes(topic));
      setGenerated(true);
    }
  };

  const handleReset = () => {
    setInputText('');
    setTopic('');
    setAssignments([]);
    setQuizzes([]);
    setGenerated(false);
  };

  const copyToClipboard = () => {
    let output = '=== ASSIGNMENTS ===\n\n';
    assignments.forEach((a, i) => {
      output += `${i + 1}. [${a.type}] ${a.question}\n\n`;
    });
    
    output += '\n=== QUIZ QUESTIONS ===\n\n';
    quizzes.forEach((q, i) => {
      output += `${i + 1}. ${q.question}\n`;
      q.options.forEach((opt, j) => {
        output += `   ${String.fromCharCode(65 + j)}) ${opt}\n`;
      });
      output += `   Correct Answer: ${String.fromCharCode(65 + q.answer)}\n\n`;
    });

    navigator.clipboard.writeText(output);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-8">
      <div className="max-w-4xl mx-auto">
        <div className="bg-white rounded-lg shadow-lg p-8 mb-6">
          <div className="flex items-center gap-3 mb-6">
            <FileText className="text-indigo-600" size={32} />
            <h1 className="text-3xl font-bold text-gray-800">
              Assignment & Quiz Generator
            </h1>
          </div>

          <div className="mb-6">
            <div className="flex gap-4 mb-4">
              <button
                onClick={() => setInputMode('text')}
                className={`px-4 py-2 rounded-lg font-medium transition ${
                  inputMode === 'text'
                    ? 'bg-indigo-600 text-white'
                    : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                }`}
              >
                Enter Document Text
              </button>
              <button
                onClick={() => setInputMode('topic')}
                className={`px-4 py-2 rounded-lg font-medium transition ${
                  inputMode === 'topic'
                    ? 'bg-indigo-600 text-white'
                    : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                }`}
              >
                Enter Topic
              </button>
            </div>

            {inputMode === 'text' ? (
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Document Text
                </label>
                <textarea
                  value={inputText}
                  onChange={(e) => setInputText(e.target.value)}
                  placeholder="Paste your document text here..."
                  className="w-full h-40 p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
                />
              </div>
            ) : (
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Topic
                </label>
                <input
                  type="text"
                  value={topic}
                  onChange={(e) => setTopic(e.target.value)}
                  placeholder="Enter a topic (e.g., Photosynthesis, World War II, Machine Learning)"
                  className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
                />
              </div>
            )}
          </div>

          <div className="flex gap-3">
            <button
              onClick={handleGenerate}
              disabled={
                (inputMode === 'text' && !inputText.trim()) ||
                (inputMode === 'topic' && !topic.trim())
              }
              className="flex-1 bg-indigo-600 text-white py-3 rounded-lg font-semibold hover:bg-indigo-700 disabled:bg-gray-300 disabled:cursor-not-allowed transition"
            >
              Generate Questions
            </button>
            {generated && (
              <>
                <button
                  onClick={copyToClipboard}
                  className="px-6 py-3 bg-green-600 text-white rounded-lg font-semibold hover:bg-green-700 transition flex items-center gap-2"
                >
                  <Copy size={20} />
                  {copied ? 'Copied!' : 'Copy'}
                </button>
                <button
                  onClick={handleReset}
                  className="px-6 py-3 bg-gray-600 text-white rounded-lg font-semibold hover:bg-gray-700 transition flex items-center gap-2"
                >
                  <RefreshCw size={20} />
                  Reset
                </button>
              </>
            )}
          </div>
        </div>

        {generated && (
          <>
            <div className="bg-white rounded-lg shadow-lg p-8 mb-6">
              <div className="flex items-center gap-2 mb-4">
                <FileText className="text-indigo-600" size={24} />
                <h2 className="text-2xl font-bold text-gray-800">Assignments</h2>
              </div>
              <div className="space-y-4">
                {assignments.map((assignment, idx) => (
                  <div key={idx} className="border-l-4 border-indigo-600 pl-4 py-2">
                    <div className="flex items-center gap-2 mb-2">
                      <span className="bg-indigo-100 text-indigo-700 px-3 py-1 rounded-full text-sm font-medium">
                        {assignment.type}
                      </span>
                      <span className="text-gray-600 font-semibold">Question {idx + 1}</span>
                    </div>
                    <p className="text-gray-700">{assignment.question}</p>
                  </div>
                ))}
              </div>
            </div>

            <div className="bg-white rounded-lg shadow-lg p-8">
              <div className="flex items-center gap-2 mb-4">
                <HelpCircle className="text-green-600" size={24} />
                <h2 className="text-2xl font-bold text-gray-800">Quiz Questions</h2>
              </div>
              <div className="space-y-6">
                {quizzes.map((quiz, idx) => (
                  <div key={idx} className="border rounded-lg p-4 bg-gray-50">
                    <p className="font-semibold text-gray-800 mb-3">
                      {idx + 1}. {quiz.question}
                    </p>
                    <div className="space-y-2 ml-4">
                      {quiz.options.map((option, optIdx) => (
                        <div
                          key={optIdx}
                          className={`p-2 rounded ${
                            optIdx === quiz.answer
                              ? 'bg-green-100 border border-green-400'
                              : 'bg-white border border-gray-300'
                          }`}
                        >
                          <div className="flex items-center gap-2">
                            <span className="font-semibold">
                              {String.fromCharCode(65 + optIdx)})
                            </span>
                            <span>{option}</span>
                            {optIdx === quiz.answer && (
                              <CheckCircle className="text-green-600 ml-auto" size={20} />
                            )}
                          </div>
                        </div>
                      ))}
                    </div>
                    <div className="mt-3 text-sm text-gray-600">
                      <span className="font-semibold">Correct Answer: </span>
                      {String.fromCharCode(65 + quiz.answer)}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </>
        )}
      </div>
    </div>
  );
};

export default AssignmentQuizGenerator;