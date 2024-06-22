import "./globals.css";
import Header from '../components/Header';

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <head>
        <title>Trade Center</title>
      </head>
      <body>
        <Header />
        <main>{children}</main>
        <footer>© 2024 Ben Gurion University</footer>
      </body>
    </html>
  );
}

