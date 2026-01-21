import streamlit as st
import random

# アプリのタイトルと説明
st.set_page_config(page_title="大学生のズボラ飯献立ナビ", page_icon="🍳")
st.title("🍳 大学生のズボラ飯献立ナビ")
st.write("冷蔵庫にあるものを入力してね。できるだけ包丁を使わない、安くて簡単なメニューを提案するよ！")

# 食材の入力
ingredients = st.text_input("冷蔵庫にある食材（例：卵, 鶏肉, キャベツ）", "")

# ズボラ飯データベース（AIに考えてもらったレシピ案）
recipe_db = [
    {"name": "爆速！親子丼風レンジ蒸し", "main": ["鶏肉", "卵"], "desc": "耐熱容器に切った鶏肉と麺つゆを入れてレンジでチン。最後に溶き卵を入れてさらに30秒！"},
    {"name": "キャベツと卵のズボラ炒め", "main": ["キャベツ", "卵"], "desc": "キャベツを手でちぎって炒め、卵を投入。塩コショウかマヨネーズで味付けするだけ。"},
    {"name": "鶏肉のポン酢さっぱり煮", "main": ["鶏肉"], "desc": "鶏肉を焼いてポン酢と砂糖少々で煮詰める。これだけで飯が進む！"},
    {"name": "無限キャベツ", "main": ["キャベツ"], "desc": "千切り（または手でちぎった）キャベツにツナ缶とごま油、鶏ガラを混ぜるだけ。"},
    {"name": "たまごかけご飯（豪華版）", "main": ["卵"], "desc": "いつものTKGに、ごま油と少しの醤油、あれば天かすをのせる。"},
    {"name": "鶏肉とキャベツのレンジ蒸し", "main": ["鶏肉", "キャベツ"], "desc": "耐熱皿にキャベツを敷き、鶏肉をのせて酒と塩を振りレンジで5分。ポン酢でどうぞ。"}
]

if st.button("献立を提案してもらう"):
    if ingredients:
        # 入力された食材が含まれているレシピを探す
        user_ingredients = [i.strip() for i in ingredients.replace("、", ",").split(",")]
        found_recipes = []
        
        for recipe in recipe_db:
            # 入力した食材のいずれかがメイン食材に含まれているかチェック
            if any(item in user_ingredients for item in recipe["main"]):
                found_recipes.append(recipe)
        
        st.subheader("今日のご飯はこれだ！")
        
        if found_recipes:
            # 該当するレシピからランダムに最大3つ表示
            display_recipes = random.sample(found_recipes, min(len(found_recipes), 3))
            for r in display_recipes:
                with st.expander(f"✨ {r['name']}"):
                    st.write(f"**使う主な食材:** {', '.join(r['main'])}")
                    st.write(f"**作り方:** {r['desc']}")
        else:
            st.warning("その食材に合うズボラ飯がまだ登録されてないみたい...。でも、適当に炒めるだけでも案外いけるよ！")
    else:
        st.error("まずは冷蔵庫にあるものを何か入力してみてね。")

# 輝さんへのメッセージ（フッター）
st.markdown("---")
st.caption("※このアプリは、自炊が面倒な大学生のためにAIと協力して作りました。")
