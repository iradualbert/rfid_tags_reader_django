import React from "react";

const Table = ({ tags }) => {
	if(tags.length === 0) {
		return null
	}
	return (
		<table className="table text-white">
			<thead>
				<tr>
					<th>Name</th>
					<th>ID</th>
					<th />
				</tr>
			</thead>
			<tbody>
				{tags.map((tag) => (
					<tr key={tag.tag_id}>
						<td>{tag.name}</td>
						<td>{tag.tag_id}</td>
					</tr>
				))}
			</tbody>
		</table>
	);
}


function Dashboard({ bagInfo }) {
	const { tags=[], missing_tags=[] } = bagInfo;
	const total = tags?.length;
	const total_missing_tags = missing_tags?.length
	return (
		<div className="row align-items-start">
			<div className="card  text-white bg-success mb-4 col-md-5 m-auto">
				<div className="card-header text-center">Total Tags</div>
				<div className="card-body">
					<h5 className="card-title text-center">
						{total} {`Tag(s)`}
					</h5>
					<Table tags={tags} />
				</div>
			</div>
			<div className="card text-center text-white bg-danger mb-4 col-md-5 m-auto">
				<div className="card-header">Missing Tags</div>
				<div className="card-body">
					<h5 className="card-title">
						{total_missing_tags} {`Tag(s)`}
					</h5>
					<Table tags={missing_tags} />
				</div>
			</div>
		</div>
	);
}

export default Dashboard;
