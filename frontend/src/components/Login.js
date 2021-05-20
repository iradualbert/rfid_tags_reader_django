import React, { useState  } from "react";
import axios from "axios";

const Login = ({ setAuthToken, setUser }) => {
	const [username, setUsername] = useState("");
	const [authKey, setAuthKey] = useState("");
	const [isLoading, setIsLoading] = useState(false);
	const [error, setError] = useState("");

	const handleSubmit = async (event) => {
		event.preventDefault();
		setIsLoading(true);
		const body = { username, auth_key: authKey }
		try {
			const { data } = await axios.post("/login", body);
			setAuthToken(data.auth_token)
			setUser(data)
		} catch (err) {
			console.log(err.response?.data?.error)
			setError(err.response?.data.error)
		}
		setIsLoading(false);

	};

	return (
		<div className="col-md-6 m-auto">
			<div className="card card-body mt-5">
				<h2 className="text-center">Kullanıcı Girişi</h2>
				<form onSubmit={handleSubmit}>
					<div className="form-group">
						<label>Kullanıcı Adı</label>
						<input
							type="text"
							className="form-control"
							name="username"
							onChange={(e) => setUsername(e.target.value)}
							value={username}
						/>
					</div>

					<div className="form-group">
						<label>Kullanıcı Kodu</label>
						<input
							type="password"
							className="form-control"
							name="Auth Key"
							onChange={(e) => setAuthKey(e.target.value)}
							value={authKey}
						/>
					</div>

					<div className="form-group">
						<br />
						{error && <div className="alert alert-danger" role="alert">
							{error}
						</div>}
						<button
							type="submit"
							disabled={isLoading || !(username && authKey)}
							className="btn btn-primary text-center"
						>
							Giriş Yap
						</button>
					</div>
				</form>
			</div>
		</div>
	);
};

export default Login;
