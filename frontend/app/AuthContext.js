// // context/AuthContext.js
// import React, { createContext, useState, useEffect } from 'react';
//
// export const AuthContext = createContext();
//
// export const AuthProvider = ({ children }) => {
//   const [token, setToken] = useState(() => {
//     return localStorage.getItem('token') || null;
//   });
//
//   useEffect(() => {
//     if (token) {
//       localStorage.setItem('token', token);
//     } else {
//       localStorage.removeItem('token');
//     }
//   }, [token]);
//
//   const value = {
//     token,
//     setToken,
//   };
//
//   return (
//     <AuthContext.Provider value={value}>
//       {children}
//     </AuthContext.Provider>
//   );
// };
