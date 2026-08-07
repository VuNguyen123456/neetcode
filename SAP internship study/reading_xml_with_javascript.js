const xml2js = require('xml2js');

const xmlData = `
<Order id="500">
  <Customer>Vu Nguyen</Customer>
  <Items>
    <Item>Widget</Item>
    <Item>Gadget</Item>
  </Items>
</Order>
`;

const parser = new xml2js.Parser();

parser.parseStringPromise(xmlData).then(result => {
  console.log(JSON.stringify(result, null, 2));
});