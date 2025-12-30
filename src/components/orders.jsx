import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

function Orders() {
  const [orders, setOrders] = useState([]);
  const [orderId, setOrderId] = useState("");
  const [customer, setCustomer] = useState("");
  const [item, setItem] = useState("");
  const navigate = useNavigate();                                      // navigating back to login from logout

  const fetchOrders = async () => {
  const res = await fetch("http://localhost:5000/orders", {                       
    credentials: "include",
  });

  // 🔥 COOKIE INVALID → LOGOUT EVERYWHERE
    if (res.status === 401) {
    navigate("/login");
    return;
  }

  const data = await res.json();
  setOrders(data);
};

  useEffect(() => {
    fetchOrders();
  }, []);

  // ===== ADD =====
  const addOrder = async () => {
    await fetch("http://localhost:5000/add-order", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      credentials: "include",                                           // using cookie to send token to backend 
      body: JSON.stringify({
        order_id: orderId,
        customer_name: customer,
        item,
      }),
    });

    fetchOrders();
  };

  // ===== UPDATE =====
  const updateOrder = async (id) => {
    const newItem = prompt("Enter new item:");
    if (!newItem) return;

    await fetch("http://localhost:5000/update-order", {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      credentials: "include",
      body: JSON.stringify({
        order_id: id,
        item: newItem,
      }),
    });

    fetchOrders();
  };

  // ===== DELETE =====
  const deleteOrder = async (id) => {
    await fetch("http://localhost:5000/delete-order", {
      method: "DELETE",
      headers: { "Content-Type": "application/json" },
      credentials: "include",
      body: JSON.stringify({ order_id: id }),
    });

    fetchOrders();
  };

  // ===== LOGOUT =====
  const logout = async () => {                                              // async await used to prevent DOM from breaking
    await fetch("http://localhost:5000/logout", {                           // async await used to prevent race conditions
      method: "POST",
      credentials: "include",
    });
    navigate("/login");
  };

  return (
    <div>
      <h2>Orders</h2>

      <input placeholder="Order ID" onChange={(e) => setOrderId(e.target.value)} />
      <input placeholder="Customer" onChange={(e) => setCustomer(e.target.value)} />
      <input placeholder="Item" onChange={(e) => setItem(e.target.value)} />
      <button onClick={addOrder}>Add Order</button>

      <br /><br />

      <table border="1">
        <thead>
          <tr>
            <th>ID</th>
            <th>Customer</th>
            <th>Item</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {orders.map((o) => (
            <tr key={o.order_id}>
              <td>{o.order_id}</td>
              <td>{o.customer_name}</td>
              <td>{o.item}</td>
              <td>
                <button onClick={() => updateOrder(o.order_id)}>Update</button>
                <button onClick={() => deleteOrder(o.order_id)}>Delete</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      <br />
      <button onClick={logout}>Logout</button>
    </div>
  );
}

export default Orders;