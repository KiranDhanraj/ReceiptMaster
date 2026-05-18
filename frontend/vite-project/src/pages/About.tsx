export default function About() {
  return (
    <div style={{ display: "flex", flexDirection: "column", gap: 24 }}>
      <h1>About</h1>
      <p>
        ReceiptWebApp helps you upload receipts, extract items, and visualize
        spending by category. It currently only supports Walmart receipts.
      </p>

      <section>
        <h2>Privacy</h2>
        <p>
          Receipts and items are only accessible to the account that uploaded
          them.
        </p>
      </section>

      <section>
        <h2>Contact</h2>
        <p>
          Please email kirandhanraj1@gmail.com with any concerns or questions.
        </p>
      </section>
    </div>
  );
}
