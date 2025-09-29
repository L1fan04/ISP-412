from fastapi import FastAPI, HTTPException, Request, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional, List
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "app.db")

app = FastAPI(title="CRUD База данных", version="1.0.0")

app.add_middleware(
	CORSMiddleware,
	allow_origins=["*"],
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)


def get_connection():
	conn = sqlite3.connect(DB_PATH)
	conn.row_factory = sqlite3.Row
	return conn


def init_db():
	os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
	conn = get_connection()
	try:
		conn.execute(
			"""
			CREATE TABLE IF NOT EXISTS items (
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				title TEXT NOT NULL,
				description TEXT
			);
			"""
		)
		conn.commit()
	finally:
		conn.close()


class ItemCreate(BaseModel):
	title: str
	description: Optional[str] = None


class Item(ItemCreate):
	id: int


@app.on_event("startup")
async def on_startup():
	init_db()


@app.get("/items", response_model=List[Item])
async def list_items():
	conn = get_connection()
	try:
		rows = conn.execute("SELECT id, title, description FROM items ORDER BY id").fetchall()
		return [Item(id=row["id"], title=row["title"], description=row["description"]) for row in rows]
	finally:
		conn.close()


@app.get("/items/{item_id}", response_model=Item)
async def get_item(item_id: int):
	conn = get_connection()
	try:
		row = conn.execute(
			"SELECT id, title, description FROM items WHERE id = ?",
			(item_id,),
		).fetchone()
		if not row:
			raise HTTPException(status_code=404, detail="Item not found")
		return Item(id=row["id"], title=row["title"], description=row["description"])
	finally:
		conn.close()


@app.post("/items", response_model=Item, status_code=201)
async def create_item(payload: ItemCreate):
	conn = get_connection()
	try:
		cur = conn.execute(
			"INSERT INTO items (title, description) VALUES (?, ?)",
			(payload.title, payload.description),
		)
		conn.commit()
		new_id = cur.lastrowid
		row = conn.execute(
			"SELECT id, title, description FROM items WHERE id = ?",
			(new_id,),
		).fetchone()
		return Item(id=row["id"], title=row["title"], description=row["description"])
	finally:
		conn.close()


@app.put("/items/{item_id}", response_model=Item)
async def update_item(item_id: int, payload: ItemCreate):
	conn = get_connection()
	try:
		cur = conn.execute(
			"UPDATE items SET title = ?, description = ? WHERE id = ?",
			(payload.title, payload.description, item_id),
		)
		conn.commit()
		if cur.rowcount == 0:
			raise HTTPException(status_code=404, detail="Item not found")
		row = conn.execute(
			"SELECT id, title, description FROM items WHERE id = ?",
			(item_id,),
		).fetchone()
		return Item(id=row["id"], title=row["title"], description=row["description"])
	finally:
		conn.close()


@app.delete("/items/{item_id}", status_code=204)
async def delete_item(item_id: int):
	conn = get_connection()
	try:
		cur = conn.execute("DELETE FROM items WHERE id = ?", (item_id,))
		conn.commit()
		if cur.rowcount == 0:
			raise HTTPException(status_code=404, detail="Item not found")
		return None
	finally:
		conn.close()


# Простая веб-страница
@app.get("/", response_class=HTMLResponse)
async def home():
	conn = get_connection()
	try:
		items = conn.execute("SELECT * FROM items ORDER BY id").fetchall()
	finally:
		conn.close()
	
	html = """
	<!DOCTYPE html>
	<html>
	<head>
		<title>CRUD База данных</title>
		<meta charset="utf-8">
		<style>
			body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
			.container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
			h1 { color: #333; text-align: center; margin-bottom: 30px; }
			.form-group { margin-bottom: 20px; }
			label { display: block; margin-bottom: 5px; font-weight: bold; color: #555; }
			input, textarea { width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 5px; font-size: 14px; }
			button { background: #007bff; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; margin-right: 10px; }
			button:hover { background: #0056b3; }
			.btn-danger { background: #dc3545; }
			.btn-danger:hover { background: #c82333; }
			.btn-success { background: #28a745; }
			.btn-success:hover { background: #218838; }
			.items { margin-top: 30px; }
			.item { background: #f8f9fa; padding: 15px; margin-bottom: 15px; border-radius: 5px; border-left: 4px solid #007bff; }
			.item h3 { margin: 0 0 10px 0; color: #333; }
			.item p { margin: 0; color: #666; }
			.item-id { font-size: 12px; color: #999; }
			.actions { margin-top: 10px; }
			.actions button { margin-right: 5px; padding: 5px 10px; font-size: 12px; }
		</style>
	</head>
	<body>
		<div class="container">
			<h1>🗄️ Управление базой данных</h1>
			
			<h2>➕ Добавить новую запись</h2>
			<form method="post" action="/add">
				<div class="form-group">
					<label for="title">Название:</label>
					<input type="text" id="title" name="title" required>
				</div>
				<div class="form-group">
					<label for="description">Описание:</label>
					<textarea id="description" name="description" rows="3"></textarea>
				</div>
				<button type="submit" class="btn-success">✅ Добавить</button>
			</form>
			
			<div class="items">
				<h2>📋 Все записи</h2>
	"""
	
	for item in items:
		desc = item["description"] if item["description"] else "Без описания"
		html += f"""
				<div class="item">
					<div class="item-id">ID: {item["id"]}</div>
					<h3>{item["title"]}</h3>
					<p>{desc}</p>
					<div class="actions">
						<button onclick="editItem({item["id"]}, '{item["title"]}', '{desc}')" class="btn-success">✏️ Редактировать</button>
						<button onclick="deleteItem({item["id"]})" class="btn-danger">🗑️ Удалить</button>
					</div>
				</div>
		"""
	
	html += """
			</div>
		</div>
		
		<script>
			function editItem(id, title, description) {
				const newTitle = prompt("Новое название:", title);
				if (newTitle === null) return;
				
				const newDescription = prompt("Новое описание:", description === "Без описания" ? "" : description);
				if (newDescription === null) return;
				
				const form = document.createElement('form');
				form.method = 'POST';
				form.action = '/edit/' + id;
				
				const titleInput = document.createElement('input');
				titleInput.type = 'hidden';
				titleInput.name = 'title';
				titleInput.value = newTitle;
				
				const descInput = document.createElement('input');
				descInput.type = 'hidden';
				descInput.name = 'description';
				descInput.value = newDescription;
				
				form.appendChild(titleInput);
				form.appendChild(descInput);
				document.body.appendChild(form);
				form.submit();
			}
			
			function deleteItem(id) {
				if (confirm('Вы уверены, что хотите удалить эту запись?')) {
					fetch('/items/' + id, { method: 'DELETE' })
						.then(() => location.reload());
				}
			}
		</script>
	</body>
	</html>
	"""
	return html


@app.post("/add")
async def add_item(title: str = Form(...), description: str = Form("")):
	conn = get_connection()
	try:
		conn.execute("INSERT INTO items (title, description) VALUES (?, ?)", (title, description or None))
		conn.commit()
	finally:
		conn.close()
	return RedirectResponse(url="/", status_code=303)


@app.post("/edit/{item_id}")
async def edit_item(item_id: int, title: str = Form(...), description: str = Form("")):
	conn = get_connection()
	try:
		cur = conn.execute("UPDATE items SET title = ?, description = ? WHERE id = ?", (title, description or None, item_id))
		conn.commit()
		if cur.rowcount == 0:
			raise HTTPException(status_code=404, detail="Item not found")
	finally:
		conn.close()
	return RedirectResponse(url="/", status_code=303)

