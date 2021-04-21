import React, { useState, useRef, useEffect } from "react";
import axios from "axios";
import "./App.css";
import Login from "./components/Login";
import DashBoard from "./components/Dashboard";
import Entry from "./components/Entry";

const baseUrl = "http://127.0.0.1:8000/api";
axios.defaults.baseURL = baseUrl;

const App = () => {
	const [authToken, setAuthToken] = useState();
	const [bagInfo, setBagInfo] = useState({});
	const [user, setUser] = useState({ username: ""});
	const loadBagInfo = useRef();
	const loadEntries = useRef();

	loadBagInfo.current = async () => {
		try {
			const { data } = await axios.get("/bag-info");
			setBagInfo(data);
		} catch (err) {
			console.log(err);
		}
	};

	loadEntries.current = async () => {
		// try {
		// 	const { data } = await axios.get("/entries", {
		// 		params: { auth_token: authToken },
		// 	});
		// 	setEntries(data);
		// } catch (err) {
		// 	console.log(err);
		// }
	};

	useEffect(() => {
		const token = localStorage.getItem("authToken");
		if (token) {
			setAuthToken(token);
		}
		loadBagInfo.current();
	}, []);

	useEffect(() => {
		if (authToken) {
			loadEntries.current();
			localStorage.setItem("authToken", authToken);
		} else {
			localStorage.removeItem("authToken");
		}
	}, [authToken]);

	// const notAuthenticated = !authToken;

	return (
		<div className="container">
			<DashBoard bagInfo={bagInfo} />
			<Entry user={user}/>
			<Login setAuthToken={setAuthToken} setUser={setUser} />
		</div>
	);
};

export default App;
