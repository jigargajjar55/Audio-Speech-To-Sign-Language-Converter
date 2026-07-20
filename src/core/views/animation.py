from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.cache import cache
from src.core.services.nlp_service import NLPService
from src.core.models import TranslationHistory

# Initialize the NLP service
nlp_service = NLPService()

@login_required(login_url="login")
def animation_view(request):
    if request.method == 'POST':
        text = request.POST.get('sen', '')
        stitched_video_path = None
        words = []
        
        if text:
            # Check Cache
            cache_key = f"stitch_{hash(text.lower())}"
            stitched_video_path = cache.get(cache_key)
            
            # Process text using the NLP service
            words = nlp_service.process_text(text)
            
            if not stitched_video_path and words:
                stitched_video_path = nlp_service.stitch_video(words)
                if stitched_video_path:
                    cache.set(cache_key, stitched_video_path, timeout=86400) # cache for 24 hrs
            
            if not words:
                messages.error(request, "Error processing text. Please try again with different words.")
            elif not stitched_video_path:
                messages.error(request, "Error stitching video clips together.")
            else:
                # Save to History
                TranslationHistory.objects.create(
                    user=request.user,
                    input_text=text,
                    stitched_video_path=stitched_video_path
                )
        
        return render(request, 'animation.html', {'words': words, 'text': text, 'stitched_video_path': stitched_video_path})
    else:
        return render(request, 'animation.html')
