import React from 'react';

const TableComponent = () => {
  
  const titles = [
    'Expenses', 'Date', 'Item', 
    'Retailer', 'Cost', 'Category'
  ];

  // Generate table rows with titles and input fields
  const tableRows = titles.map((title, index) => (
    <tr key={index}>
      <td>{title}</td>
      <td><input type="text" placeholder={`Input ${index + 1}`} /></td>
    </tr>
  ));

  return (
    <table border="1">
      <tbody>
        {tableRows}
      </tbody>
    </table>
  );
}

export default TableComponent;