import React from "react";

import "./../styles/glossary.css";

import data from "./../services/data";

export default function Glossary() {
	return (
		<div className="glossary">
			<div className="glossary-header">
				<h3>Glossary of</h3>
				<h1>Technical Indicators</h1>
			</div>

			{data.glossary.detailText.map((sec) => (
				<section id={sec.id} key={sec.heading} className="glossary-section glossary-detail-text">
					<div className="glossary-detail-text-heading">
						<h1>{sec.heading}</h1>

						<hr />

						<img
							className="glossary-img"
							src={sec.imgSrc}
							style={{
								width: "35vw",
								height: "40vh",
								marginRight: "2vw",
							}}
							alt="RSI"
						/>
					</div>

					<div className="glossary-detail-text-content">
						{sec.content.map((line) => (
							<p className="detail-text-list-line" key={sec.content.indexOf(line)}>
								{line}
							</p>
						))}
					</div>
				</section>
			))}

			{/* <div className="glossary-img-section">
				<img
					className="glossary-img"
					src={require("../assets/img/rsi.png")}
					style={{
						width: "45vw",
						height: "40vh",
						marginRight: "2vw",
					}}
					alt="RSI Image"
				/>
				<img
					className="glossary-img"
					src={require("../assets/img/macd.png")}
					style={{
						width: "45vw",
						height: "40vh",
					}}
					alt="RSI Image"
				/>
			</div> */}
		</div>
	);
}
