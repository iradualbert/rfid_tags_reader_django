import React from "react";
import dayjs from "dayjs";
import relativeTime from "dayjs/plugin/relativeTime";
import "dayjs/locale/tr";
import Table from "./Table";

dayjs.extend(relativeTime);
dayjs.locale('tr')

const parseTime = time => {
	return dayjs(time).fromNow()
}

const History = ({ entries }) => {
	const extractor = (item) => {
		const { taken_at, taken, total } = item;
		return [parseTime(taken_at), total, taken];
	};
	return (
        <>
            <br />
            <h2>History</h2>
			<Table
				data={entries}
				titles={["Saat", "Toplam", "Alınan Takımları"]}
				extractor={extractor}
			/>
		</>
	);
};

export default History;
