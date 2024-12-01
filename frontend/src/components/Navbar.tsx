import { Link } from 'react-router-dom';

const Navbar = () => {
  return (
    <nav className="bg-white/70 backdrop-blur-sm shadow">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
        <div className="flex justify-between items-center">
          <Link to="/" className="text-3xl font-extrabold text-gray-900">
            <span className="text-indigo-600">LingoGrade</span>
          </Link>
          <div className="flex items-center">
            <Link
              to="/login"
              className="px-8 py-3 text-base font-medium rounded-md text-indigo-600 bg-white hover:bg-gray-50 border border-indigo-600"
            >
              Login
            </Link>
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar; 