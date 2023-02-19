import "./App.css";
import { Navigate, Route, Routes } from "react-router-dom";

import Header from "./components/Header";
import Landing from "./components/Landing";
import Glossary from "./components/Glossary";
import Footer from "./components/Footer";

export default function App() {
	return (
		<div className="App">
			<Header />

			<Routes>
				<Route path="/" element={<Landing />} />

				<Route path="/glossary" element={<Glossary />} />

				<Route path="*" element={<Navigate replace to="/" />} />
			</Routes>

			<Footer />
		</div>
	);
}
