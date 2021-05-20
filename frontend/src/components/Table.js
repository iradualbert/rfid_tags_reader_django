import React from "react";

const Table = ({ titles, data, extractor }) => {
	return (
		<table className="table ">
			<thead>
				<tr>
					{titles.map((title) => (
						<th key={title}>{title}</th>
					))}
				</tr>
			</thead>
			<tbody>
				{data.map((item) => {
					const row = extractor(item);
					return (
						<tr key={row[0]}>
							{row.map((col) => (
								<td key={col}>{col}</td>
							))}
						</tr>
					);
				})}
			</tbody>
		</table>
	);
};

export default Table;
