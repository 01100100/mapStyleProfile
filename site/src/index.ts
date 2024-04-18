import * as echarts from "echarts/core";
import data from "../../timing_results.json";

interface Style {
  load_time: number;
  screenshot: string;
  style_id: string;
  style_name: string;
  style_url: string;
}

const styleArray: Style[] = data as Style[];

import {
  DatasetComponent,
  TooltipComponent,
  GridComponent,
  VisualMapComponent,
  TransformComponent,
} from "echarts/components";
import { BarChart } from "echarts/charts";
import { CanvasRenderer } from "echarts/renderers";

echarts.use([
  DatasetComponent,
  TooltipComponent,
  GridComponent,
  VisualMapComponent,
  TransformComponent,
  BarChart,
  CanvasRenderer,
]);
console.log(styleArray);
var chartDom = document.getElementById("main");
var myChart = echarts.init(chartDom);
var option;
option = {
  dataset: [
    {
      dimensions: ["style_name", "load_time"],
      source: styleArray,
    },
    {
      transform: {
        type: "sort",
        config: { dimension: "style_name", order: "asc" },
      },
    },
  ],

  yAxis: { type: "category", inverse: true, axisLabel: false },
  xAxis: {
    type: "value",
    name: "loading time (ms)",
    nameLocation: "center",
    nameGap: 30,
  },
  visualMap: {
    show: false,
    min: 5000,
    max: 1000,
    dimension: 1,
    inRange: {
      color: ["#65B581", "#FFCE34", "#FD665F"],
    },
  },
  series: {
    type: "bar",
    encode: { y: "style_name", x: "load_time" },
    label: {
      show: true,
      precision: 1,
      position: "right",
      valueAnimation: true,
      fontFamily: "monospace",
      formatter: "{b}",
    },
  },
  tooltip: {},
};

console.log(option);
myChart.setOption(option);
myChart.on("click", function (params) {
  var x: Style = params.data as Style;
  const div = document.getElementById("info");
  div.innerHTML = "";
  const img = document.createElement("img");
  img.src = x.screenshot;
  div.appendChild(img);
  const p = document.createElement("p");
  p.textContent = `Style Name: ${x.style_name}`;
  div.appendChild(p);
  const p2 = document.createElement("p");
  p2.textContent = `Style ID: ${x.style_id}`;
  div.appendChild(p2);
  const p3 = document.createElement("p");
  p3.textContent = `Style URL: ${x.style_url}`;
  div.appendChild(p3);
  const p4 = document.createElement("p");
  p4.textContent = `Load Time: ${x.load_time} ms`;
  div.appendChild(p4);
});
