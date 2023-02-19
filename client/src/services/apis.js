const API_ROOT = "https://3598-2409-40c1-1006-bf37-9c88-e0b9-9c15-d3ea.ngrok.io";

async function getCompanyInfo(obj) {
	return fetch(
		`${API_ROOT}/getCompanyInfo?name=${obj.name}&ticker=${obj.ticker}&interval=${obj.interval}&period=${obj.period}`,
		{
			method: "GET",
		}
	);
}

async function getIndicatorInfo(obj) {
	return fetch(
		`${API_ROOT}/getIndicatorInfo?name=${obj.name}&ticker=${obj.ticker}&interval=${obj.interval}&period=${obj.period}&indicator=${obj.indicator}`,
		{
			method: "GET",
		}
	);
}

async function getNewsInfo(obj) {
	return fetch(`${API_ROOT}/getCompanyNews?name=${obj.name}`, {
		method: "GET",
	});
}

const apis = {
	// auth: { login, register, forget, email },
	// user: { getAllUsers, getMyProfile, getUserById, getProfList },
	company: {
		getCompanyInfo,
		getIndicatorInfo,
		getNewsInfo,
	},
};

export default apis;
