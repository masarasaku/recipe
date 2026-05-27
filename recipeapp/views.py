# recipeapp/views.py
from django.shortcuts import render
import google.generativeai as genai
from .models import UserSeasoning

def index(request):
    # --- 1. 初期表示（GET）のときにDBから調味料を取得 ---
    saved_seasonings = []
    if request.user.is_authenticated:
        try:
            user_seasoning = UserSeasoning.objects.get(user=request.user)
            saved_seasonings = [s.strip() for s in user_seasoning.saved_seasoning.split(",")]
        except UserSeasoning.DoesNotExist:
            pass 

    # --- 2. ボタンが押されたとき（POST）の処理 ---
    if request.method == 'POST':
        ingredients = request.POST.get('ingredients')
        
        # 画面のチェックボックスで選ばれた調味料を取得
        selected_seasonings = request.POST.getlist('seasonings')
        
        # その他に入力があればリストに合流
        other_seasonings = request.POST.get('other_seasonings')
        if other_seasonings:
            selected_seasonings.append(other_seasonings)
            
        # ---------------------------------------------------------------
        # 最新の調味料をデータベースに保存・更新する
        # ---------------------------------------------------------------
        if request.user.is_authenticated:
            seasoning_data_to_save = ",".join(selected_seasonings)
            UserSeasoning.objects.update_or_create(
                user=request.user,
                defaults={'saved_seasoning': seasoning_data_to_save}
            )
        # ---------------------------------------------------------------

        # AIへ渡すための文字列（見た目調整用）
        seasonings_str = ", ".join(selected_seasonings) if selected_seasonings else "なし（水・油のみ使用可）"
        
        # Gemini API の呼び出し処理
        model = genai.GenerativeModel()
        
        # 🔥 プロンプトを調整：詳細手順と区切り文字を追加
        prompt = f"""
以下の食材と調味料を使って、家庭で簡単に作れる献立とレシピを提案してください。
テキストの装飾にmarkdown（## や ***）は一切使わないでください。

【使用する食材】
{ingredients}

【使える調味料】
{seasonings_str}

【絶対条件】
1. 味付けには、必ず上記の【使える調味料】にリストアップされているもの「だけ」を使用してください。リストにない調味料は絶対にレシピに含めないでください。
2. ダラダラとした挨拶（「承知いたしました」など）の文章は一切不要です。いきなり【出力フォーマット】の形で出力してください。

【出力フォーマット】
🍳 料理名：[ここに料理名]
⏱️ 調理時間：[〇〇分] / 難易度：[★☆☆☆☆（簡単！）]

■ 準備する食材
・[食材を箇条書き]

■ 使う調味料
・[使う調味料を箇条書き]

■ パパッと3ステップ調理手順
1. 【切る】[15文字以内で簡潔に]
2. 【炒める/煮る】[15文字以内で簡潔に]
3. 【仕上げ】[15文字以内で簡潔に]

💡 AIからのワンポイント：
[なぜこの調味料の組み合わせにしたのかなどを1行で]

===詳細手順===
1. 【切る詳細】
[初心者が迷わないよう、具体的な食材の切り方、下ごしらえのコツを具体的に説明してください]
2. 【炒める/煮る詳細】
[フライパンの火加減（強火・中火・弱火など）や、調味料を入れるタイミング、焼き色などの状態の目安を交えて具体的に説明してください]
3. 【仕上げ詳細】
[タレの煮詰め具合、盛り付けのコツなど、完成までの流れを具体的に説明してください]
"""
        
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )
        
        # 🔥 レスポンスを区切り文字「===詳細手順===」で分割する処理を追加
        ai_response = response.text
        if "===詳細手順===" in ai_response:
            main_recipe, detailed_steps = ai_response.split("===詳細手順===", 1)
        else:
            main_recipe = ai_response
            detailed_steps = ""

        context = {
            'ingredients': ingredients,
            'result': main_recipe.strip(),          # 今までのパパッと見れる部分
            'detailed_steps': detailed_steps.strip(),# 【追加】具体的な詳細手順
        }
        return render(request, 'recipeapp/recipe_result.html', context)

    # --- 3. 普通に画面を開いた（GET）ときの処理 ---
    context = {
        'saved_seasonings': saved_seasonings,
    }       
    return render(request, 'recipeapp/index.html', context)