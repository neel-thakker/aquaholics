import React from "react";
import { Link } from "react-router-dom";

import "../styles/header.css";

export default function Header() {
	return (
		<div className="header">
			<Link to="/" className="header-logo">
				<div className="header-company">
					<img
						className="header-company-img"
						src={require("../assets/img/logo.png")}
						alt="Logo"
						height={"60vh"}
						width={"60vw"}
					/>
					<h1 className="header-company-name">Stock Instructor</h1>
				</div>
			</Link>

			<Link to="/glossary" className="navbar-item">
				Glossary{" "}
			</Link>
		</div>
	);
}
