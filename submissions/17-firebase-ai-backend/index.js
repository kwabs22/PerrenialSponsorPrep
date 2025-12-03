/**
 * Firebase AI Backend
 * Showcases: Vertex AI Integration
 */
const { initializeApp } = require('firebase/app');
const { getVertexAI, getGenerativeModel } = require('firebase/vertexai');

const firebaseConfig = {
  apiKey: process.env.FIREBASE_API_KEY,
  projectId: process.env.FIREBASE_PROJECT_ID,
};

const app = initializeApp(firebaseConfig);
const vertexAI = getVertexAI(app);

async function main() {
  console.log('='.repeat(50));
  console.log('Firebase AI Backend');
  console.log('='.repeat(50));

  const model = getGenerativeModel(vertexAI, { model: 'gemini-1.5-flash' });

  // Generate text
  const prompt = 'Write a short greeting for a mobile app';
  const result = await model.generateContent(prompt);
  console.log('\n🤖 AI Response:', result.response.text());

  // Chat session
  const chat = model.startChat();
  const chatResult = await chat.sendMessage('What features should a productivity app have?');
  console.log('\n💬 Chat:', chatResult.response.text());
}

main().catch(console.error);
