import React from 'react';
import Plot from 'react-plotly.js';

interface Props {
  grades: Record<string, number>;
}

export const GradesChart: React.FC<Props> = ({ grades }) => {
  const categories = Object.keys(grades);
  const values = Object.values(grades);
  
  // Complete the circle
  categories.push(categories[0]);
  values.push(values[0]);

  return (
    <Plot
      data={[{
        type: 'scatterpolar',
        r: values,
        theta: categories,
        fill: 'toself',
        name: 'Grades'
      }]}
      layout={{
        polar: {
          radialaxis: {
            visible: true,
            range: [0, 1]
          }
        },
        showlegend: false,
        width: 400,
        height: 400
      }}
    />
  );
}; 