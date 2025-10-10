import React, { useEffect, useState } from "react";
import api from "../api";
import ProductCard from "./ProductCard";
import { Link } from "react-router-dom";
// export default function ProductList() {
//   const [products, setProducts] = useState([]);
//   const [q, setQ] = useState("");
//   const [suggestions, setSuggestions] = useState([]);

//   useEffect(() => {
//     fetchProducts();
//   }, []);

//   async function fetchProducts() {
//     try {
//       const res = await api.get("/api/products/");
//       setProducts(res.data);
//     } catch (err) {
//       console.error(err);
//     }
//   }

//   const handleSearchChange = (e) => {
//     const value = e.target.value;
//     setQ(value);
//     if (!value) {
//       setSuggestions([]);
//       return;
//     }
//     const filtered = products.filter(p => p.name.toLowerCase().includes(value.toLowerCase()));
//     setSuggestions(filtered.slice(0, 6));
//   };

//   const displayed = q ? products.filter(p => p.name.toLowerCase().includes(q.toLowerCase())) : products;

//   return (
//     <div>
//       <h2>Products</h2>
//       <div style={{ marginBottom: 12 }}>
//         <input type="text" placeholder="Search products..." value={q} onChange={handleSearchChange} />
//       </div>

//       {suggestions.length > 0 && (
//         <div style={{ position: "absolute", background: "#fff", border: "1px solid #ccc", zIndex: 1000 }}>
//           {suggestions.map(s => (
//             <div key={s.id} style={{ padding: 8 }}>
//               <a href={`/product/${s.id}`}>{s.name}</a>
//             </div>
//           ))}
//         </div>
//       )}

//       <div className="card-container">
//         {displayed.length ? displayed.map(p => <ProductCard key={p.id} product={p} />) : <p>No products.</p>}
//       </div>
//     </div>
//   );
// }


//  second fix

// import React, { useEffect, useState } from "react";
// import { Link } from "react-router-dom";
// import api from "../api";
// import ProductCard from "./ProductCard";

// export default function ProductList() {
//   const [products, setProducts] = useState([]);
//   const [q, setQ] = useState("");
//   const [suggestions, setSuggestions] = useState([]);

//   useEffect(() => {
//     fetchProducts();
//   }, []);

//   async function fetchProducts() {
//     try {
//       const res = await api.get("/api/products/");
//       setProducts(res.data);
//     } catch (err) {
//       console.error(err);
//     }
//   }

//   const handleSearchChange = (e) => {
//     const value = e.target.value;
//     setQ(value);
//     if (!value) {
//       setSuggestions([]);
//       return;
//     }
//     const filtered = products.filter((p) =>
//       p.name.toLowerCase().includes(value.toLowerCase())
//     );
//     setSuggestions(filtered.slice(0, 6));
//   };

//   const displayed = q
//     ? products.filter((p) =>
//         p.name.toLowerCase().includes(q.toLowerCase())
//       )
//     : products;

//   return (
//     <div>
//       <h2>Products</h2>
//       <div style={{ marginBottom: 12 }}>
//         <input
//           type="text"
//           placeholder="Search products..."
//           value={q}
//           onChange={handleSearchChange}
//         />
//       </div>

//       {suggestions.length > 0 && (
//         <div
//           style={{
//             position: "absolute",
//             background: "#fff",
//             border: "1px solid #ccc",
//             zIndex: 1000,
//             width: "300px",
//           }}
//         >
//           {suggestions.map((s) => (
//             <div key={s.id} style={{ padding: 8 }}>
//               <Link to={`/product/${s.id}`} style={{ textDecoration: "none" }}>
//                 {s.name}
//               </Link>
//             </div>
//           ))}
//         </div>
//       )}

//       <div className="card-container">
//         {displayed.length ? (
//           displayed.map((p) => <ProductCard key={p.id} product={p} />)
//         ) : (
//           <p>No products found.</p>
//         )}
//       </div>
//     </div>
//   );
// }


// ----------------------------fix 3-------------------------

// import React, { useEffect, useState } from "react";
// import { Link } from "react-router-dom";
// import api from "../api";
// import ProductCard from "./ProductCard";

// export default function ProductList() {
//   const [products, setProducts] = useState([]);
//   const [filtered, setFiltered] = useState([]);
//   const [userProfile, setUserProfile] = useState(null);
//   const [q, setQ] = useState("");
//   const [suggestions, setSuggestions] = useState([]);

//   useEffect(() => {
//     fetchProducts();
//     fetchUserProfile();
//   }, []);

//   async function fetchUserProfile() {
//     try {
//       const res = await api.get("/api/profile/");
//       setUserProfile(res.data);
//     } catch (err) {
//       console.warn("No profile found (maybe user not logged in)");
//     }
//   }

//   async function fetchProducts() {
//     try {
//       const res = await api.get("/api/products/");
//       setProducts(res.data);
//     } catch (err) {
//       console.error(err);
//     }
//   }

//   // Filter based on user’s hobby/interest
//   useEffect(() => {
//     if (!userProfile || !products.length) return;
//     const { hobby, interest } = userProfile;

//     const personalized = products.filter(
//       (p) =>
//         (p.category && (p.category.toLowerCase().includes(hobby?.toLowerCase()) ||
//           p.category.toLowerCase().includes(interest?.toLowerCase()))) ||
//         (p.description && (p.description.toLowerCase().includes(hobby?.toLowerCase()) ||
//           p.description.toLowerCase().includes(interest?.toLowerCase())))
//     );

//     // Combine personalized at top + rest
//     const combined = [...personalized, ...products.filter(p => !personalized.includes(p))];
//     setFiltered(combined);
//   }, [userProfile, products]);

//   const handleSearchChange = (e) => {
//     const value = e.target.value;
//     setQ(value);
//     if (!value) {
//       setSuggestions([]);
//       return;
//     }
//     const filtered = products.filter((p) =>
//       p.name.toLowerCase().includes(value.toLowerCase())
//     );
//     setSuggestions(filtered.slice(0, 6));
//   };

//   const displayed = q
//     ? products.filter((p) =>
//         p.name.toLowerCase().includes(q.toLowerCase())
//       )
//     : filtered.length
//     ? filtered
//     : products;

//   return (
//     <div>
//       <h2>Products</h2>
//       <div style={{ marginBottom: 12 }}>
//         <input
//           type="text"
//           placeholder="Search products..."
//           value={q}
//           onChange={handleSearchChange}
//         />
//       </div>

//       {suggestions.length > 0 && (
//         <div
//           style={{
//             position: "absolute",
//             background: "#fff",
//             border: "1px solid #ccc",
//             zIndex: 1000,
//             width: "300px",
//           }}
//         >
//           {suggestions.map((s) => (
//             <div key={s.id} style={{ padding: 8 }}>
//               <Link to={`/products/${s.id}`} style={{ textDecoration: "none" }}>
//                 {s.name}
//               </Link>
//             </div>
//           ))}
//         </div>
//       )}

//       <div className="card-container">
//         {displayed.length ? (
//           displayed.map((p) => <ProductCard key={p.id} product={p} />)
//         ) : (
//           <p>No products found.</p>
//         )}
//       </div>
//     </div>
//   );
// }



// ------fix 4-----------

// src/components/ProductList.jsx
// import React, { useEffect, useState } from "react";
// import api from "../api";
// import ProductCard from "./ProductCard";

// export default function ProductList() {
//   const [products, setProducts] = useState([]);
//   const [q, setQ] = useState("");
//   const [suggestions, setSuggestions] = useState([]);
//   const [profile, setProfile] = useState(null);

//   useEffect(() => {
//     fetchProfileAndProducts();
//   }, []);

//   // ✅ Fetch logged-in user's profile (hobby + interest)
//   async function fetchProfileAndProducts() {
//     try {
//       const token = localStorage.getItem("access");
//       if (token) {
//         const res = await api.get("/api/profile/", {
//           headers: { Authorization: `Bearer ${token}` },
//         });
//         setProfile(res.data);
//         // Now fetch products filtered by hobby/interest
//         fetchProducts(res.data.profile?.hobby, res.data.profile?.interest);
//       } else {
//         // not logged in — fetch all
//         fetchProducts();
//       }
//     } catch (err) {
//       console.warn("Profile fetch failed, loading all products.");
//       fetchProducts();
//     }
//   }

//   // ✅ Fetch products (optionally filtered by hobby/interest)
//   async function fetchProducts(hobby = "", interest = "") {
//     try {
//       let url = "/api/products/";
//       if (hobby || interest) {
//         const params = [];
//         if (hobby) params.push(`hobby=${encodeURIComponent(hobby)}`);
//         if (interest) params.push(`interest=${encodeURIComponent(interest)}`);
//         url += "?" + params.join("&");
//       }

//       const res = await api.get(url);
//       setProducts(res.data);
//     } catch (err) {
//       console.error("Product fetch error:", err);
//     }
//   }

//   // ✅ Handle search
//   const handleSearchChange = (e) => {
//     const value = e.target.value;
//     setQ(value);
//     if (!value) {
//       setSuggestions([]);
//       return;
//     }
//     const filtered = products.filter((p) =>
//       p.name.toLowerCase().includes(value.toLowerCase())
//     );
//     setSuggestions(filtered.slice(0, 6));
//   };

//   const displayed = q
//     ? products.filter((p) => p.name.toLowerCase().includes(q.toLowerCase()))
//     : products;

//   return (
//     <div>
//       <h2>
//         {profile
//           ? `Welcome, ${profile.username}! Showing products based on your interests.`
//           : "Products"}
//       </h2>

//       <div style={{ marginBottom: 12 }}>
//         <input
//           type="text"
//           placeholder="Search products..."
//           value={q}
//           onChange={handleSearchChange}
//         />
//       </div>

//       {/* ✅ Search suggestions */}
//       {suggestions.length > 0 && (
//         <div
//           style={{
//             position: "absolute",
//             background: "#fff",
//             border: "1px solid #ccc",
//             zIndex: 1000,
//             width: "60%",
//           }}
//         >
//           {suggestions.map((s) => (
//             <div key={s.id} style={{ padding: 8 }}>
//               <a href={`/product/${s.id}`}>{s.name}</a>
//             </div>
//           ))}
//         </div>
//       )}

//       {/* ✅ Product grid */}
//       <div className="card-container">
//         {displayed.length ? (
//           displayed.map((p) => <ProductCard key={p.id} product={p} />)
//         ) : (
//           <p>No products available.</p>
//         )}
//       </div>
//     </div>
//   );
// }



// ==================fix 5========================

// src/components/ProductList.jsx
// import React, { useEffect, useState } from "react";
// import { Link } from "react-router-dom";
// import api from "../api";
// import ProductCard from "./ProductCard";

export default function ProductList() {
  const [products, setProducts] = useState([]);
  const [q, setQ] = useState("");
  const [suggestions, setSuggestions] = useState([]);
  const [userProfile, setUserProfile] = useState(null);

  useEffect(() => {
    loadProfileAndProducts();
  }, []);

  // ✅ Load both user profile (if logged in) and products
  async function loadProfileAndProducts() {
    try {
      const token = localStorage.getItem("access");
      if (token) {
        const res = await api.get("/api/profile/", {
          headers: { Authorization: `Bearer ${token}` },
        });
        setUserProfile(res.data.profile);
        await fetchProducts(res.data.profile?.hobby, res.data.profile?.interest);
      } else {
        await fetchProducts(); // guest mode
      }
    } catch (err) {
      console.warn("Profile fetch failed → showing all products");
      await fetchProducts();
    }
  }

  // ✅ Fetch products (auto-filter by backend using hobby/interest)
  async function fetchProducts(hobby = "", interest = "") {
    try {
      const res = await api.get("/api/products/");
      setProducts(res.data);
    } catch (err) {
      console.error("Product fetch error:", err);
    }
  }

  // ✅ Handle live search box
  const handleSearchChange = (e) => {
    const value = e.target.value;
    setQ(value);
    if (!value) {
      setSuggestions([]);
      return;
    }
    const filtered = products.filter((p) =>
      p.name.toLowerCase().includes(value.toLowerCase())
    );
    setSuggestions(filtered.slice(0, 6));
  };

  const displayed = q
    ? products.filter((p) => p.name.toLowerCase().includes(q.toLowerCase()))
    : products;

  return (
    <div>
      <h2>
        {userProfile
          ? `Welcome back! Showing products related to your hobby: ${userProfile.hobby} and interest: ${userProfile.interest}.`
          : "All Products"}
      </h2>

      {/* ✅ Search input */}
      <div style={{ marginBottom: 12, position: "relative" }}>
        <input
          type="text"
          placeholder="Search products..."
          value={q}
          onChange={handleSearchChange}
          style={{
            width: "60%",
            padding: "8px",
            borderRadius: "5px",
            border: "1px solid #ccc",
          }}
        />

        {/* ✅ Dropdown search suggestions */}
        {suggestions.length > 0 && (
          <div
            style={{
              position: "absolute",
              top: "100%",
              left: 0,
              width: "60%",
              background: "#fff",
              border: "1px solid #ccc",
              borderTop: "none",
              zIndex: 1000,
            }}
          >
            {suggestions.map((s) => (
              <div
                key={s.id}
                style={{
                  padding: "8px",
                  cursor: "pointer",
                  borderBottom: "1px solid #eee",
                }}
              >
                <Link
                  to={`/product/${s.id}`}
                  style={{ textDecoration: "none", color: "#333" }}
                >
                  {s.name}
                </Link>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* ✅ Product grid */}
      <div className="card-container">
        {displayed.length ? (
          displayed.map((p) => <ProductCard key={p.id} product={p} />)
        ) : (
          <p>No products found.</p>
        )}
      </div>
    </div>
  );
}


