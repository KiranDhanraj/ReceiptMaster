export default function Help() {
  return (
    <div style={{ display: "flex", flexDirection: "column", gap: 24 }}>
      <h1>Help</h1>

      <section>
        <h2>How to Upload</h2>
        <p>
          Go to Upload, choose a receipt image, and click Upload. You will see a
          success message when it is processed. Please note that there is a limited amount of tokens
          and an error will occur when the limit is reached. 
        </p>
      </section>

      <section>
        <h2>Charts and Categories</h2>
        <p>
          The pie chart shows your spending by category for the receipts you
          selected. Click a category to view product details.
        </p>
      </section>

      <section>
        <h2>Missing Product Data</h2>
        <p>
          If a barcode is unknown, product details may show as N/A. This happens
          when the external lookup does not have a match.
        </p>
      </section>

      <section>
        <h2>Deleting Receipts</h2>
        <p>
          Use the Delete button next to a receipt. You will be asked to confirm
          before removal.
        </p>
      </section>
    </div>
  );
}
