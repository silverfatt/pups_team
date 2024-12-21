import React from "react";
import { Pie } from "react-chartjs-2";
import { Chart, ArcElement, Tooltip, Legend } from "chart.js";
import ChartDataLabels from "chartjs-plugin-datalabels";

Chart.register(ArcElement, Tooltip, Legend, ChartDataLabels);

export default function PieChart({ data }) {
  const chartData = {
    labels: Object.keys(data),
    datasets: [
      {
        data: Object.values(data),
        backgroundColor: [
          "rgba(75,192,192,1)",
          "rgba(75,192,150,0.8)",
          "rgba(75,192,192,0.6)",
          
        ].reverse(),
        borderWidth: 1,
      },
    ],
  };

  const options = {
    plugins: {
      legend: {
        position: "bottom",
        labels: {
          boxWidth: 30,
          padding: 15,
        },
      },
      tooltip: {
        enabled: true,
      },
      datalabels: {
        color: "#fff",
        font: {
          size: 30,
          weight: "bold",
        },
        formatter: (value) => value,
        anchor: "center",
        align: "center",
      },
    },
    maintainAspectRatio: false,
  };

  return (
    <div style={{ width: "100%", height: "400px" }}>
      <Pie data={chartData} options={options} />
    </div>
  );
}
