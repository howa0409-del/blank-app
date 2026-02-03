import streamlit as st
import random
from supabase import create_client, Client

# --- 1. Supabaseへの接続設定 ---
# SecretsからURLとキーを読み込む
url = st.secrets["supabase"]["url"]
key = st.secrets["supabase"]["key"]
supabase: Client = create_client(url, key)

# --- アプリの基本設定 ---
st.set_page_config(page_title="大学生のズボラ飯献立ナビ", page_icon="🍳")
st.title("🍳 大学生のズボラ飯献立ナビ + 保存機能")
st.write("冷蔵庫にあるものを入力してね。気に入ったレシピはデータベースに保存できるよ！")

# --- ズボラ飯データベース（内蔵データ） ---
recipe_db = [
    {"name": "爆速！親子丼風レンジ蒸し", "main": ["鶏肉", "卵"], "desc": "鶏肉と麺つゆをレンジでチン。最後に溶き卵を入れてさらに30秒！"},
    {"name": "キャベツと卵のズボラ炒め", "main": ["キャベツ", "卵"], "desc": "キャベツをちぎって炒め、卵を投入。マヨネーズで味付け。"},
    {"name": "鶏肉のポン酢さっぱり煮", "main": ["鶏肉"], "desc": "鶏肉を焼いてポン酢と砂糖少々で煮詰めるだけ。"},
    {"name": "無限キャベツ", "main": ["キャベツ"], "desc": "ちぎったキャベツにツナ缶、ごま油、鶏ガラを混ぜる。"},
    {"name": "たまごかけご飯（豪華版）", "main": ["卵"], "desc": "TKGに、ごま油と醤油、天かすをのせる。"},
    {"name": "鶏肉とキャベツのレンジ蒸し", "main": ["鶏肉", "キャベツ"], "desc": "キャベツの上に鶏肉をのせ、酒と塩を振りレンジで5分。"}
]

# --- 2. 機能の実装 ---

# タブで画面を切り替えられるようにする
tab1, tab2 = st.tabs(["🔍 レシピ検索", "⭐ お気に入り一覧"])

with tab1:
    ingredients = st.text_input("冷蔵庫にある食材（例：卵, 鶏肉, キャベツ）", "")
    
    if st.button("献立を提案してもらう"):
        if ingredients:
            user_ingredients = [i.strip() for i in ingredients.replace("、", ",").split(",")]
            found_recipes = []
            
            for recipe in recipe_db:
                if any(item in user_ingredients for item in recipe["main"]):
                    found_recipes.append(recipe)
            
            st.subheader("今日のご飯はこれだ！")
            
            if found_recipes:
                display_recipes = random.sample(found_recipes, min(len(found_recipes), 3))
                for r in display_recipes:
                    with st.container():
                        st.markdown(f"### ✨ {r['name']}")
                        st.write(f"**作り方:** {r['desc']}")
                        
                        # --- データベースへの保存ボタン ---
                        # ボタンを押すとSupabaseにデータが飛ぶ仕組み
                        if st.button("お気に入りに保存", key=f"save_{r['name']}"):
                            try:
                                data = {"recipe_name": r['name'], "ingredients": ", ".join(r['main'])}
                                supabase.table("favorites").insert(data).execute()
                                st.success(f"「{r['name']}」を保存しました！タブを切り替えて見てみてね。")
                            except Exception as e:
                                st.error(f"保存に失敗しました...: {e}")
                        st.divider()
            else:
                st.warning("その食材に合うレシピが見つからない...適当に炒めちゃおう！")
        else:
            st.error("食材を入力してね。")

with tab2:
    st.subheader("保存したお気に入りレシピ")
    
    # --- データベースからの読み込み ---
    # 更新ボタンを押すと最新データを取得
    if st.button("リストを更新"):
        pass # ボタンを押すだけで再読み込みが走るため処理は空でOK
    
    try:
        # Supabaseから全データを取得するコード
        response = supabase.table("favorites").select("*").execute()
        rows = response.data
        
        if rows:
            for row in rows:
                st.info(f"**{row['recipe_name']}** （主な食材: {row['ingredients']}）")
        else:
            st.write("まだ保存されたレシピはありません。")
            
    except Exception as e:
        st.error("データの読み込みに失敗しました。Secretsの設定を確認してね。")

st.markdown("---")
st.caption("Using Supabase Database")
