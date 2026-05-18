import { useEffect, useMemo, useState } from "react";
import { PieChart, Pie, Cell, Tooltip, Legend, ResponsiveContainer } from "recharts";
import api from "../services/api";

type Receipt = {
  id: number;
  created_at: string;
  number: number;
};

type CategoryStat = {
  category: string;
  total: number;
};

type CategoryItem = {
  name: string;
  price: number;
  description: string;
};

const COLORS = ["#1b4332", "#2d6a4f", "#52b788", "#74c69d", "#95d5b2", "#b7e4c7"];

export default function Dashboard() {
  const [receipts, setReceipts] = useState<Receipt[]>([]);
  const [selectedIds, setSelectedIds] = useState<number[]>([]);
  const [stats, setStats] = useState<CategoryStat[]>([]);
  const [selectedCategory, setSelectedCategory] = useState<string | null>(null);
  const [categoryItems, setCategoryItems] = useState<CategoryItem[]>([]);
  const [error, setError] = useState("");

  useEffect(() => {
    const loadReceipts = async () => {
      try {
        const response = await api.get("/receipts");
        setReceipts(response.data);
        setSelectedIds(response.data.map((receipt: Receipt) => receipt.id));
      } catch (err) {
        setError("Failed to load receipts");
      }
    };
    loadReceipts();
  }, []);

  useEffect(() => {
    const loadStats = async () => {
      try {
        const response = await api.post("/stats/categories", {
          receipt_ids: selectedIds.length ? selectedIds : null,
        });
        setStats(response.data);
      } catch (err) {
        setError("Failed to load stats");
      }
    };
    loadStats();
  }, [selectedIds]);

  useEffect(() => {
    const loadCategoryItems = async () => {
      if (!selectedCategory) {
        setCategoryItems([]);
        return;
      }
      try {
        const response = await api.post("/stats/category-items", {
          category: selectedCategory,
          receipt_ids: selectedIds.length ? selectedIds : null,
        });
        setCategoryItems(response.data);
      } catch (err) {
        setError("Failed to load category items");
      }
    };
    loadCategoryItems();
  }, [selectedCategory, selectedIds]);

  const totalSpend = useMemo(
    () => stats.reduce((sum, item) => sum + item.total, 0),
    [stats]
  );

  const handleToggle = (receiptId: number) => {
    setSelectedIds((current) =>
      current.includes(receiptId)
        ? current.filter((id) => id !== receiptId)
        : [...current, receiptId]
    );
  };

  const handleDelete = async (receiptId: number) => {
    const confirmed = window.confirm("Delete this receipt? This cannot be undone.");
    if (!confirmed) {
      return;
    }
    try {
      await api.delete(`/receipts/${receiptId}`);
      setReceipts((current) => current.filter((receipt) => receipt.id !== receiptId));
      setSelectedIds((current) => current.filter((id) => id !== receiptId));
    } catch (err) {
      setError("Failed to delete receipt");
    }
  };

  const allSelected = receipts.length > 0 && selectedIds.length === receipts.length;

  return (
    <div>
      <h1>Dashboard</h1>

      <div style={{ display: "flex", gap: 24, alignItems: "flex-start" }}>
        <section style={{ flex: 2, height: 360, marginBottom: 48 }}>
          <h2>Spending by Category</h2>
          {stats.length === 0 ? (
            <p>No data for selected receipts.</p>
          ) : (
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={stats}
                  dataKey="total"
                  nameKey="category"
                  outerRadius={120}
                  label={({ name, percent }) => `${name} ${(percent * 100).toFixed(1)}%`}
                  onClick={(data) => setSelectedCategory(data.name)}
                >
                  {stats.map((entry, index) => (
                    <Cell key={entry.category} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip formatter={(value: number) => `$${value.toFixed(2)}`} />
                <Legend />
              </PieChart>
            </ResponsiveContainer>
          )}
          {totalSpend > 0 ? <p>Total: ${totalSpend.toFixed(2)}</p> : null}
        </section>

        <section style={{ flex: 1 }}>
          <h2>Receipts</h2>
          {receipts.length === 0 ? (
            <p>No receipts available.</p>
          ) : (
            <div>
              <button
                type="button"
                onClick={() =>
                  setSelectedIds(allSelected ? [] : receipts.map((receipt) => receipt.id))
                }
              >
                {allSelected ? "Clear all" : "Select all"}
              </button>

              {receipts.map((receipt) => (
                <div key={receipt.id} style={{ display: "flex", alignItems: "center", gap: 8 }}>
                  <label style={{ display: "flex", alignItems: "center", gap: 6 }}>
                    <input
                      type="checkbox"
                      checked={selectedIds.includes(receipt.id)}
                      onChange={() => handleToggle(receipt.id)}
                    />
                    Receipt {receipt.number} - {new Date(receipt.created_at).toLocaleDateString()}
                  </label>
                  <button type="button" onClick={() => handleDelete(receipt.id)}>
                    Delete
                  </button>
                </div>
              ))}
            </div>
          )}
        </section>
      </div>

      <section style={{ marginTop: 32 }}>
        <h2>
          {selectedCategory
            ? `Products in ${selectedCategory}`
            : "Select a category to see products"}
        </h2>
        {selectedCategory && categoryItems.length === 0 ? (
          <p>No products for this category.</p>
        ) : null}
        {categoryItems.length > 0 ? (
          <div style={{ overflowX: "auto" }}>
            <table
              style={{
                width: "100%",
                borderCollapse: "collapse",
                fontFamily: "Consolas, 'Courier New', monospace",
              }}
            >
              <thead>
                <tr style={{ backgroundColor: "#f2f2f2" }}>
                  <th style={{ textAlign: "left", padding: "8px", border: "1px solid #ccc" }}>
                    Name
                  </th>
                  <th style={{ textAlign: "right", padding: "8px", border: "1px solid #ccc" }}>
                    Price
                  </th>
                  <th style={{ textAlign: "left", padding: "8px", border: "1px solid #ccc" }}>
                    Description
                  </th>
                </tr>
              </thead>
              <tbody>
                {categoryItems.map((item, index) => (
                  <tr key={`${item.name}-${item.price}-${index}`}>
                    <td style={{ padding: "8px", border: "1px solid #ccc" }}>
                      {item.name}
                    </td>
                    <td
                      style={{
                        padding: "8px",
                        border: "1px solid #ccc",
                        textAlign: "right",
                        minWidth: 80,
                      }}
                    >
                      ${item.price.toFixed(2)}
                    </td>
                    <td style={{ padding: "8px", border: "1px solid #ccc" }}>
                      <details>
                        <summary>View</summary>
                        <p>{item.description}</p>
                      </details>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : null}
      </section>

      {error ? <p>{error}</p> : null}
    </div>
  );
}