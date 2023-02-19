import React, { useEffect, useState } from "react";

import { TextField, Autocomplete, MenuItem, Backdrop, CircularProgress } from "@mui/material";
import AutorenewIcon from "@mui/icons-material/Autorenew";

import ReactApexChart from "react-apexcharts";
import ReactSpeedometer from "react-d3-speedometer";

import apis from "../services/apis";
import data from "../services/data";

export default function Landing() {
	const [isLoading, setIsLoading] = useState(false);
	const [isOpaqueLoading, setIsOpaqueLoading] = useState(false);

	const [companyInfo, setCompanyInfo] = useState(null);
	const [indicatorInfo, setIndicatorInfo] = useState(null);
	const [newsInfo, setNewsInfo] = useState(Array(0));

	const [searchCompany, setSearchCompany] = useState({
		name: "",
	});
	const [interval, setInterval] = useState("");
	const [period, setPeriod] = useState("");
	const [indicator, setIndicator] = useState("");

	const defaultProps = {
		options: data.searchCompany.companies,
		getOptionLabel: (option) => option.name,
	};

	const updateCompanyInfo = async () => {
		setIndicator("");
		setIndicatorInfo(null);
		setIsOpaqueLoading(true);

		try {
			const obj = {
				name: searchCompany,
				ticker: searchCompany
					? data.searchCompany.companies.find((com) => com.name === searchCompany).symbol
					: "",
				interval: interval ? data.searchCompany.intervals.find((com) => com.name === interval).code : "1m",
				period: period ? data.searchCompany.periods.find((com) => com.name === period).code : "1d",
			};

			console.log(JSON.stringify(obj, 4, 4));

			let response = await apis.company.getCompanyInfo(obj).then((res) => res.json());

			console.log(JSON.stringify(response, 4, 4));

			setCompanyInfo(response);
		} catch (err) {
			console.log(err, "in updateCompanyInfo inside DocsPage");
			alert("An error occurred, please try again some time");
		}

		updateNewsInfo();
		setIsOpaqueLoading(false);
	};

	useEffect(() => {
		if (!indicator || indicator === "") return () => {};
		updateIndicatorInfo();
	}, [indicator]);

	const updateIndicatorInfo = async () => {
		setIsLoading(true);

		try {
			const obj = {
				name: searchCompany,
				ticker: searchCompany
					? data.searchCompany.companies.find((com) => com.name === searchCompany).symbol
					: "",
				interval: interval ? data.searchCompany.intervals.find((com) => com.name === interval).code : "1m",
				period: period ? data.searchCompany.periods.find((com) => com.name === period).code : "1d",
				indicator: indicator.substring(0, 3) + indicator.substring(6, 8),
			};

			console.log(JSON.stringify(obj, 4, 4));

			let response = await apis.company.getIndicatorInfo(obj).then((res) => res.json());

			console.log(JSON.stringify(response, 4, 4));

			setIndicatorInfo(response);
		} catch (err) {
			console.log(err, "in updateCompanyInfo inside DocsPage");
			alert("An error occurred, please try again some time");
		}

		setIsLoading(false);
	};

	const updateNewsInfo = async () => {
		setIsLoading(true);

		try {
			const obj = {
				name: searchCompany,
			};

			console.log(JSON.stringify(obj, 4, 4));

			let response = await apis.company.getNewsInfo(obj).then((res) => res.json());

			console.log(JSON.stringify(response, 4, 4));

			setNewsInfo(response);
		} catch (err) {
			console.log(err, "in updateCompanyInfo inside DocsPage");
			alert("An error occurred, please try again some time");
		}

		setIsLoading(false);
	};

	return (
		<>
			<Backdrop sx={{ color: "white", zIndex: "1301" }} open={isLoading}>
				<CircularProgress color="inherit" />
			</Backdrop>

			<Backdrop
				sx={{ color: data.font.yellow500, zIndex: "1302", backgroundColor: "#fff", opacity: "0.4" }}
				open={isOpaqueLoading}>
				<CircularProgress color="inherit" />
			</Backdrop>

			<div className="searchbar">
				<Autocomplete
					{...defaultProps}
					id="searchbar-autocomplete"
					// defaultValue={searchCompany}
					onChange={(e) => setSearchCompany(e.target.innerHTML)}
					sx={{ width: 500, backgroundColor: "white" }}
					renderInput={(params) => <TextField {...params} label="Company name" />}
				/>

				<TextField
					sx={{ width: 150, marginLeft: "2vw", backgroundColor: "white" }}
					className="searchbar-filters-interval"
					name="Interval"
					label="Interval"
					select
					value={interval}
					onChange={(e) => setInterval(e.target.value)}>
					{data.searchCompany.intervals.map((item) => (
						<MenuItem value={item.name} key={item.code}>
							{item.name}
						</MenuItem>
					))}
				</TextField>

				<TextField
					sx={{ width: 150, marginLeft: "2vw", backgroundColor: "white" }}
					className="searchbar-filters-period"
					name="Period"
					label="Period"
					select
					value={period}
					onChange={(e) => setPeriod(e.target.value)}>
					{data.searchCompany.periods.map((item) => (
						<MenuItem value={item.name} key={item.code}>
							{item.name}
						</MenuItem>
					))}
				</TextField>

				<div className="searchbar-filters-submit">
					<AutorenewIcon
						// sx={{ backgroundColor: "white" }}
						className="submit-icon"
						fontSize="medium"
						onClick={updateCompanyInfo}
					/>
				</div>
			</div>

			{companyInfo ? (
				<div className="company">
					<h2 className="company-name">
						{companyInfo.name} ({companyInfo.ticker})
					</h2>

					<hr className="company-hr" />

					<div className="company-values">
						<h1 className="company-currVal">{companyInfo.currVal} </h1>
						<h3
							className="company-changeVal"
							style={{ color: companyInfo.changeVal > 0 ? "green" : "red" }}>
							{companyInfo.changeVal > 0 ? "+" : ""}
							{companyInfo.changeVal} ({companyInfo.changeVal > 0 ? "+" : ""}
							{companyInfo.percentChange}%)
						</h3>

						<TextField
							sx={{ width: 150, marginLeft: "auto", backgroundColor: "white" }}
							className="company-indicator-select"
							name="Indicator No.1"
							label="Indicator No.1"
							select
							value={indicator}
							onChange={(e) => setIndicator(e.target.value)}>
							{data.indicators.select.map((item) => (
								<MenuItem value={item.name} key={item.name}>
									{item.name}
								</MenuItem>
							))}
						</TextField>
					</div>

					<h6 className="company-note">In INR</h6>

					<div id="chart">
						<ReactApexChart
							// options={data.dummyCompany.charts.options}
							options={data.options.options}
							// series={data.dummyCompany.charts.series}
							// series={data.options.series}
							series={[
								{
									name: !indicator ? "Indicator" : indicator,
									type: "line",
									color: data.font.blue,
									data: !indicatorInfo
										? companyInfo.data.map((d) => {
												return {
													x: new Date(d.x),
													y: NaN,
												};
										  })
										: indicatorInfo.data.map((d) => {
												return {
													x: new Date(d.x),
													y: d.y,
												};
										  }),
								},
								{
									name: "candle",
									type: "candlestick",
									color: data.font.red,
									data: companyInfo.data.map((d) => {
										return {
											x: new Date(d.x),
											y: d.y,
										};
									}),
								},
							]}
							type="line"
							height={350}
						/>
					</div>

					<div id="chart-bar">
						<ReactApexChart
							// series={data.barGraph.series}
							// options={data.barGraph.options}
							series={[
								{
									name: "Volume",
									data: companyInfo.data.map((d) => d.v),
								},
							]}
							options={{
								chart: data.barGraph.chart,
								plotOptions: data.barGraph.plotOptions,
								dataLabels: data.barGraph.dataLabels,
								yaxis: data.barGraph.yaxis,
								title: data.barGraph.title,
								xaxis: {
									// categories: [
									// 	"Jan",
									// 	"Feb",
									// 	"Mar",
									// 	"Apr",
									// 	"May",
									// 	"Jun",
									// 	"Jul",
									// 	"Aug",
									// 	"Sep",
									// 	"Oct",
									// 	"Nov",
									// 	"Dec",
									// ],
									categories: companyInfo.data.map((d) => {
										let date = new Date(d.x);
										if (companyInfo.data.indexOf(d) % 5 === 0)
											return date.getHours() + ":" + date.getMinutes();
										else return "";
									}),
									position: "bottom",
									axisBorder: {
										show: false,
									},
									axisTicks: {
										show: false,
									},
									crosshairs: {
										fill: {
											type: "gradient",
											gradient: {
												colorFrom: "#D8E3F0",
												colorTo: "#BED1E6",
												stops: [0, 100],
												opacityFrom: 0.4,
												opacityTo: 0.5,
											},
										},
									},
									tooltip: {
										enabled: true,
									},
								},
							}}
							type="bar"
							height={350}
						/>
					</div>

					<div id="chart-line">
						<ReactApexChart
							// series={data.barGraph.series}
							// options={data.barGraph.options}
							series={[
								{
									name: "Relative Strength Index",
									data: companyInfo.data.map((d) => d.r),
								},
							]}
							options={{
								chart: {
									height: 350,
									type: "line",
									zoom: {
										enabled: true,
									},
								},
								dataLabels: {
									enabled: false,
								},
								stroke: {
									curve: "straight",
								},
								title: {
									text: "Relative Strength Index",
									align: "center",
									position: "bottom",
								},
								grid: {
									row: {
										colors: ["#f3f3f3", "transparent"], // takes an array which will be repeated on columns
										opacity: 0.5,
									},
								},
								xaxis: {
									categories: companyInfo.data.map((d) => {
										let date = new Date(d.x);
										if (companyInfo.data.indexOf(d) % 5 === 0)
											return date.getHours() + ":" + date.getMinutes();
										else return "";
									}),
								},
							}}
						/>
					</div>

					<hr className="company-hr" />

					<div className="company-predictions">
						<h2 className="company-predictions-heading">Our Predictions:</h2>
						<div className="company-prediction-gauges">
							<ReactSpeedometer
								width={500}
								needleHeightRatio={0.7}
								value={companyInfo.shortPrediction * 10}
								currentValueText="Short Term"
								customSegmentLabels={[
									{
										text: "Strong SELL",
										position: "INSIDE",
										color: "#555",
									},
									{
										text: "Weak SELL",
										position: "INSIDE",
										color: "#555",
									},
									{
										text: "HOLD",
										position: "INSIDE",
										color: "#555",
										fontSize: "19px",
									},
									{
										text: "Weak BUY",
										position: "INSIDE",
										color: "#555",
									},
									{
										text: "Strong BUY",
										position: "INSIDE",
										color: "#555",
									},
								]}
								ringWidth={47}
								needleTransitionDuration={3333}
								needleTransition="easeElastic"
								needleColor={"#90f2ff"}
								textColor={data.font.primaryText}
							/>
							<ReactSpeedometer
								width={500}
								needleHeightRatio={0.7}
								value={companyInfo.longPrediction * 10}
								currentValueText="Long Term"
								customSegmentLabels={[
									{
										text: "Strong SELL",
										position: "INSIDE",
										color: "#555",
									},
									{
										text: "Weak SELL",
										position: "INSIDE",
										color: "#555",
									},
									{
										text: "HOLD",
										position: "INSIDE",
										color: "#555",
										fontSize: "19px",
									},
									{
										text: "Weak BUY",
										position: "INSIDE",
										color: "#555",
									},
									{
										text: "Strong BUY",
										position: "INSIDE",
										color: "#555",
									},
								]}
								ringWidth={47}
								needleTransitionDuration={3333}
								needleTransition="easeElastic"
								needleColor={"#90f2ff"}
								textColor={data.font.primaryText}
							/>
						</div>
					</div>

					<hr className="company-hr" />

					<div className="company-analysis">
						<h2 className="company-analysis-heading">Our Analysis:</h2>

						{companyInfo.analysis.map((ana) => {
							return (
								<h3 className="company-analysis-list" key={ana}>
									📌 {ana}
								</h3>
							);
						})}
					</div>

					<hr className="company-hr" />

					{newsInfo ? (
						<>
							<h3 className="news-heading">📢 News</h3>

							{newsInfo.map((n) => {
								return (
									<div className="news-card" key={n.title}>
										<img
											className="news-card-img"
											src={n.urlToImg}
											alt="Denim Jeans"
											width={"30%"}
										/>

										<div className="news-card-body">
											<p className="news-source">{n.source}</p>

											<h3 className="news-title">{n.tittle}</h3>

											<p className="news-content">{n.content}</p>

											<p className="news-publishedAt">
												{n.publishedAt.substring(8, 10) +
													"/" +
													n.publishedAt.substring(5, 7) +
													"/" +
													n.publishedAt.substring(0, 4)}
											</p>
											<p>
												<button onClick={() => (window.location.href = n.url)}>
													Go to News
												</button>
											</p>
										</div>
									</div>
								);
							})}
						</>
					) : (
						<></>
					)}
				</div>
			) : (
				<div className="companyHolder"></div>
			)}
		</>
	);
}
