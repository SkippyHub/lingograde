import { Link } from 'react-router-dom';
import Navbar from '../components/Navbar';
import { Radar } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  RadialLinearScale,
  PointElement,
  LineElement,
  Filler,
  Tooltip,
  Legend
} from 'chart.js';

// Register ChartJS components
ChartJS.register(
  RadialLinearScale,
  PointElement,
  LineElement,
  Filler,
  Tooltip,
  Legend
);

const LandingPage = () => {
  const sampleData = {
    labels: ['Pronunciation', 'Fluency', 'Coherence', 'Grammar', 'Vocabulary'],
    datasets: [
      {
        label: 'Sample Progress',
        data: [85, 90, 75, 80, 85],
        backgroundColor: 'rgba(99, 102, 241, 0.2)',
        borderColor: 'rgb(99, 102, 241)',
        borderWidth: 2,
        fill: true,
      },
    ],
  };

  const chartOptions = {
    scales: {
      r: {
        beginAtZero: true,
        max: 100,
        ticks: {
          stepSize: 20,
          color: '#6B7280',
        },
      },
    },
    plugins: {
      legend: {
        display: false,
      },
    },
  };

  return (
    <div 
      className="min-h-screen bg-cover bg-center" 
      style={{ backgroundImage: 'url(/assets/images/background.jpg)' }}
    >
      <Navbar />
      
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="py-20">
          <div className="text-center">
            <h1 className="text-4xl tracking-tight font-extrabold text-gray-900 sm:text-5xl md:text-6xl">
              <span className="block">Improve Your Language Skills</span>
              <span className="block text-indigo-600">with LingoGrade</span>
            </h1>
            <p className="mt-3 max-w-md mx-auto text-base text-gray-500 sm:text-lg md:mt-5 md:text-xl md:max-w-3xl">
              Get instant feedback on your pronunciation and speaking skills. Practice, track progress, and achieve fluency faster.
            </p>
            <div className="mt-5 max-w-md mx-auto sm:flex sm:justify-center md:mt-8">
              <div className="rounded-md shadow">
                <Link
                  to="/sign-up"
                  className="w-full flex items-center justify-center px-8 py-3 border border-transparent text-base font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 md:py-4 md:text-lg md:px-10"
                >
                  Get Started
                </Link>
              </div>

            </div>
          </div>

          {/* Features Section */}
          <div className="mt-20">
            <div className="grid grid-cols-1 gap-8 sm:grid-cols-2 lg:grid-cols-3">
              <div className="pt-6">
                <div className="flow-root bg-white rounded-lg px-6 pb-8">
                  <div className="-mt-6">
                    <div className="inline-flex items-center justify-center p-3 bg-indigo-500 rounded-md shadow-lg">
                      <span className="h-full w-full flex items-center justify-center text-2xl">🎯</span>
                    </div>
                    <h3 className="mt-8 text-lg font-medium text-gray-900 tracking-tight">AI-Powered Feedback</h3>
                    <div className="mt-4 flex justify-center">
                      <img 
                        src="/assets/Google_Gemini_logo.svg.png" 
                        alt="Google Gemini AI" 
                        className="h-12 object-contain"
                      />
                    </div>
                    <p className="mt-4 text-base text-gray-500">
                      Get detailed analysis of your speaking skills powered by Google's Gemini AI model, providing professional-grade feedback on pronunciation, fluency, and more.
                    </p>
                  </div>
                </div>
              </div>

              <div className="pt-6">
                <div className="flow-root bg-white rounded-lg px-6 pb-8">
                  <div className="-mt-6">
                    <div className="inline-flex items-center justify-center p-3 bg-indigo-500 rounded-md shadow-lg">
                      <span className="h-full w-full flex items-center justify-center text-2xl">📈</span>
                    </div>
                    <h3 className="mt-8 text-lg font-medium text-gray-900 tracking-tight">Track Progress</h3>
                    <p className="mt-5 text-base text-gray-500">
                      Monitor your improvement over time with detailed analytics.
                    </p>
                    <div className="mt-6 flex justify-center items-center">
                      <div className="w-48 h-48">
                        <Radar data={sampleData} options={chartOptions} />
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <div className="pt-6">
                <div className="flow-root bg-white rounded-lg px-6 pb-8">
                  <div className="-mt-6">
                    <div className="inline-flex items-center justify-center p-3 bg-indigo-500 rounded-md shadow-lg">
                      <span className="h-full w-full flex items-center justify-center text-2xl">🌟</span>
                    </div>
                    <h3 className="mt-8 text-lg font-medium text-gray-900 tracking-tight">International Standards</h3>
                    
                    {/* Badges with Certificate */}
                    <div className="mt-4 flex items-center justify-center space-x-6">
                      <img 
                        src="/assets/CertificateSVG.svg" 
                        alt="Certificate" 
                        className="w-24 h-24 object-contain flex-shrink-0"
                      />
                      <div className="flex gap-4">
                        <span className="font-bold text-2xl text-indigo-600">CEFR</span>
                        <span className="font-bold text-2xl text-indigo-600">•</span>
                        <span className="font-bold text-2xl text-indigo-600">IELTS</span>
                      </div>
                    </div>

                    {/* Description */}
                    <p className="mt-4 text-base text-gray-500">
                      Receive feedback aligned with international language proficiency standards, helping you prepare for IELTS exams and achieve your target CEFR level.
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
};

export default LandingPage; 