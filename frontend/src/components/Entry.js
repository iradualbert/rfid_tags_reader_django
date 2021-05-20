import React, { useState } from "react";

const areas = [
	{
		name: "Uçak",
		works: [
			{
				name: "TC 100",
				tools: [],
			},
			{
				name: "TC 101",
				tools: [],
			},
			{
				name: "TC 102",
				tools: [],
			},
			{
				name: "TC 103",
				tools: [],
			},
			{
				name: "TC 104",
				tools: [],
			},
		],
	},
	{
		name: "Atölye",
		works: [
			{
				name: "Elekrik Atölysesi",
				tools: [],
			},
			{
				name: "Motor Atölyesi",
				tools: [],
			},
			{
				name: "Hidrolik Atölyesi",
				tools: [],
			},
			{
				name: "Gövde Atölyesi",
				tools: [],
			},
			{
				name: "Elektronik Atölyesi",
				tools: [],
			},
		],
	},
	{
		name: "Her Hangi",
		works: [],
	},
];

const works = [
	{
		name: "Work 1",
		tags: ["Pense", "Yıldız Tornavida", "Yan keski"],
		
	},
	{
		name: "Work 2",
		tags: ["Pense 2", "Yıldız Tornavida 2", "Yan keski 2"],
	},
	{
		name: "Work 3",
		tags: ["Pense 3", "Yıldız Tornavida 3", "Yan keski 3"],
	},
	{
		name: "Work 4",
		tags: ["Pense 4", "Yıldız Tornavida 4", "Yan keski"],
	},
	{
		name: "Work 5",
		tags: ["Pense 5", "Yıldız Tornavida", "Yan keski 6"],
	},
];

const Entry = ({ user, logout }) => {
	const [placeId, setPlaceId] = useState();
	const [workId, setWorkId] = useState();
	const [chosenWork, setChosenWork] = useState(null);
	const [isOpen, setIsOpen] = useState(false);
	const [takenTags, setTakenTags] = useState(
		["Pense 4", "Pense", "Yıldız Tornavida 4", "Yan keski"]
	);

	const onPlaceClick = (idx) => {
		const newState = idx === placeId ? undefined : idx;
		setPlaceId(newState);
		setWorkId(undefined);
	};
	const onWorkClick = (idx) => {
		const newState = idx === workId ? undefined : idx;
		setWorkId(newState);
	};

	const _onWorkClick = (idx) => {
		if (chosenWork === idx) {
			setChosenWork(null);
		} else {
			setChosenWork(idx);
		}
	};

	const fullname = user.first_name || user.username;
	return (
		<div className="row">
			<h2>Merhaba {fullname}, Nerede Çalışacaksınız? </h2>

			<div className="col-md-4">
				{areas.map((place, idx) => {
					const btnClassName =
						idx === placeId ? "btn btn-primary" : "btn btn-outline-primary";
					return (
						<button
							onClick={() => onPlaceClick(idx)}
							key={place.name}
							className={btnClassName}
						>
							{place.name}
						</button>
					);
				})}
			</div>
			{placeId !== undefined && (
				<div className="col-md-4">
					{areas[placeId].works.map((work, idx) => {
						const isSelected = idx === workId;
						const btnClassName = isSelected
							? "btn btn-primary"
							: "btn btn-outline-primary";
						return (
							<div>
								<button
									className={btnClassName}
									onClick={() => onWorkClick(idx)}
									key={work.name}
								>
									{work.name}
								</button>
							</div>
						);
					})}
				</div>
			)}
			<div className="col-md-10">

			</div>
			<div className="col-md-4">
				<button
					className="btn btn-info"
					onClick={() => setIsOpen((prev) => !prev)}
				>
					Hangi İş
				</button>
			</div>
			<div className="row col-md-10">
				{isOpen && (
					<>
						<div className="col-md-5">
							{works.map((work, idx) => {
								const isSelected = chosenWork === idx;
								const btnClassName = isSelected
									? "btn btn-primary"
									: "btn btn-outline-primary";
								return (
									<div>
										<button
											className={btnClassName}
											onClick={() => _onWorkClick(idx)}
											key={idx}
										>
											{work.name}
										</button>
										{isSelected && (
											<p className="h4 p-3">
												Lorem ipsum dolor sit amet consectetur adipisicing elit.
												Eum iure recusandae quibusdam, illum quia fugit
												architecto
											</p>
										)}
									</div>
								);
							})}
						</div>
						{chosenWork !== null && (
							<div className="col-md-4">
								{works[chosenWork].tags.map((tag, idx) => {
									const btnClass = takenTags.includes(tag) ? "btn btn-outline-success" : "btn btn-outline-danger"
									return (
										<button className={btnClass} key={idx} disabled>
											{tag}
										</button>
									);
								})}
							</div>
						)}
					</>
				)}
			</div>

			<div>
				<button
					className="btn btn-danger text-center"
					onClick={logout}
					style={{ width: 200 }}
				>
					Çıkış Yap
				</button>
			</div>
		</div>
	);
};

export default Entry;
