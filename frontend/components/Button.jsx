export default function Button({ children, onClick, className }) {
    return (
      <button onClick={onClick} className={`bg-red-600 text-white py-2 px-4 rounded ${className}`}>
        {children}
      </button>
    );

}
