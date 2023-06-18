import React, { useState, useEffect } from "react";
import Moment from "moment";

const DateTime = () => {
    const [date, setDate] = useState(Moment());

    useEffect(() => {
        const interval = setInterval(() => {
            setDate(Moment());
        }, 1000);

        return () => {
            clearInterval(interval);
        };
    }, []);

    return (
        <div>
            <h1 style={{ textAlign: "center" }}>{date.format("dddd, MMMM Do YYYY")}</h1>
            <h3 style={{ textAlign: "center" }}>{date.format("hh:mm:ss A")}</h3>
        </div>
    );
};

export default DateTime;