import React, { useState } from "react";

const areas = [
	{
		name: "Uçak",
		works: [
			{
				name: "1.Landing Gear ",
				tools: ["1. Tool", "2.Tool"],
			},
			{
				name: "2.Engine",
				tools: ["1. Tool", "2.Tool"],
			},
		],
	},
	{
		name: "Atölye",
		works: [
			{
				name: "1. Work Atolye ",
				tools: ["1. Tool", "2.Tool"],
			},
			{
				name: "2. Atolye Work ",
				tools: ["1. Tool", "2.Tool"],
			},
		],
	},
	{
		name: "Her Hangi",
		works: [],
	},
];

const Entry = ({ user }) => {
	const [placeId, setPlaceId] = useState();
    const [workId, setWorkId] = useState();
    
    const onPlaceClick = (idx) => {
        const newState = idx === placeId ? undefined : idx;
        setPlaceId(newState);
        setWorkId(undefined);
    }
	const onWorkClick = (idx) => {
		const newState = idx === workId ? undefined : idx;
		setWorkId(newState);
    };
    
    const fullname = user.first_name || user.username
	return (
        <div className="row">
            <h2>Merhaba {fullname}, Nerede Çalışacaksınız?</h2>
			<div className="col-md-4">
				{areas.map((place, idx) => {
					const btnClassName =
						idx === placeId ? "btn btn-primary" : "btn btn-light";
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
							: "btn btn-light";
						return (
							<div>
								<button
									className={btnClassName}
									onClick={() => onWorkClick(idx)}
									key={work.name}
								>
									{work.name}
								</button>
								{isSelected ? (
									<ul>
										{work.tools.map((tool) => (
											<li>{tool}</li>
										))}
									</ul>
								) : null}
							</div>
						);
					})}
				</div>
			)}
		</div>
	);
};

export default Entry;
