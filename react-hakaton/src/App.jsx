import PieChart from "./components/PieChart";
import LineChart from "./components/LineChart";
import "./index.css";
import React, { useCallback, useEffect, useState } from "react";
import dateService from "./service/date-service";

export default function App() {
  const [pieData, setPieData] = useState([]);
  const [lineData, setLineData] = useState([]);
  const [lineData1, setLineData1] = useState([]);
  const [lineData2, setLineData2] = useState([]);
  const [lineData3, setLineData3] = useState([]);
  const [reviewData, setReviewData] = useState("");
  const [response, setResponse] = useState("");

  useEffect(() => {
    dateService.getMonthName().then(setPieData);
    dateService.getLineData().then(setLineData);
    dateService.getLineDataCurrent(0).then(setLineData1);
    dateService.getLineDataCurrent(1).then(setLineData2);
    dateService.getLineDataCurrent(2).then(setLineData3);
  }, []);

  return (
    <>
      <div
        style={{
          width: "100vw",
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          justifyContent: "center",
        }}
      >
        <h1 style={{ textAlign: "center" }}>Дашборд по ИКС</h1>
        <div className="wrapper-app">
          <div className="pie-chart-container">
            <h2 style={{ textAlign: "center" }}>Распределение по категориям</h2>
            <PieChart data={pieData} />
          </div>
          <div className="line-chart-container">
            <h2 style={{ textAlign: "center" }}>
              Количество отзывов по месяцам
            </h2>
            <LineChart data={lineData} />
          </div>
          <div className="line-chart-container">
            <h2 style={{ textAlign: "center" }}>
              Количество отзывов по месяцам негативных
            </h2>
            <LineChart data={lineData1} />
          </div>
          <div className="line-chart-container">
            <h2 style={{ textAlign: "center" }}>
              Количество отзывов по месяцам нейтральных
            </h2>
            <LineChart data={lineData2} />
          </div>
          <div className="line-chart-container">
            <h2 style={{ textAlign: "center" }}>
              Количество отзывов по месяцам позитивных
            </h2>
            <LineChart data={lineData3} />
          </div>
        </div>
      </div>
      <div style={{ display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", marginTop: "20px" }}>
        <label for="story">Введите запрос:</label>
        <textarea onChange={(e) => setReviewData(e.target.value)} id="story" name="story" r style={{ marginBottom: "10px", width: "500px", height: "300px" }}>
          {reviewData}
        </textarea>
        <button
          onClick={() => dateService.getReview(reviewData).then(res => setResponse(res))}
        >
          Получить данные
        </button>
        {response.length > 0 && <span style={{ marginTop: "20px", marginBottom: "20px", width: "500px", borderRadius: "10px", padding: "10px", backgroundColor: "lightgray", whiteSpace: "pre-wrap" }}>{response}</span>}
      </div>
    </>
  );
}
