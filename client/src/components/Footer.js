import React from "react";

import "../styles/footer.css";

export default function Footer() {
	return (
		<div className="footer">
			<hr />
			<p className="footer-msg">
				<span className="footer-msg-hl">Stock Instructor</span> maps complex stock price data to an everyday
				scale that the result of us can understand Made in 🇮🇳 with ♥ by{" "}
				<span className="footer-msg-hl">Aquaholics</span>
			</p>
		</div>
	);
}
