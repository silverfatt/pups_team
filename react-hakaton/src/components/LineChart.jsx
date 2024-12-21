import React, { useRef, useEffect } from "react";
import { Line } from "react-chartjs-2";
import { Chart, LineElement, CategoryScale, LinearScale, PointElement, Tooltip, Legend, Filler } from "chart.js";

Chart.register(LineElement, CategoryScale, LinearScale, PointElement, Tooltip, Legend, Filler);

export default function LineChart({ data }) {
  const chartRef = useRef(null);

  const chartData = {
    labels: Object.keys(data),
    datasets: [
      {
        label: "Данные",
        data: Object.values(data),
        fill: true,
        backgroundColor: (context) => {
          const chart = context.chart;
          const { ctx, chartArea } = chart;

          if (!chartArea) {
            // Возвращаем пустой цвет, если область графика еще не определена
            return null;
          }

          const gradient = ctx.createLinearGradient(0, chartArea.bottom, 0, chartArea.top);
          gradient.addColorStop(0, "rgba(75,192,192,0.2)");
          gradient.addColorStop(1, "rgba(75,192,192,0.8)");
          return gradient;
        },
        borderColor: "rgba(75,192,192,1)",
        tension: 0.4,
        pointBackgroundColor: "rgba(75,192,192,1)",
      },
    ],
  };

  const options = {
    responsive: true,
    plugins: {
      legend: {
        display: true,
        position: "top",
      },
      tooltip: {
        enabled: true,
      },
    },
    scales: {
      x: {
        title: {
          display: true,
          text: "Дата",
        },
      },
      y: {
        title: {
          display: true,
          text: "Количество отзывов",
        },
        beginAtZero: true,
      },
    },
  };

  return (
    <div style={{ width: "100%", height: "400px", display: "flex", justifyContent: "center", alignItems: "center" }}>
      <Line ref={chartRef} data={chartData} options={options} />
    </div>
  );
} 