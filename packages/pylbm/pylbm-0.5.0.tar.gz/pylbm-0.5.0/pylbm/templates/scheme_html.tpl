<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/css/bootstrap.min.css" rel="stylesheet"
    integrity="sha384-giJF6kkoqNQ00vy+HMDP7azOuL0xtbfIcaT9wjKHr8RbDVddVHyTfAAsrekwKmP1" crossorigin="anonymous">

<div class="m-3">

    <div class="row d-flex justify-content-center">
        <div class="card m-2 col d-flex justify-content-center">
            <div class="card-body">
                <h5 class="card-title text-center mb-3">Dimension</h5>
                <p class="card-text text-center fs-1">${{ scheme.dim
                    }}$</p>
            </div>
        </div>
        <div class="card m-2 col">
            <div class="card-body">
                <h5 class="card-title text-center mb-3">Number of schemes</h5>
                <p class="card-text text-center fs-1">${{
                    scheme.nschemes }}$
                </p>
            </div>
        </div>
        <div class="card m-2 col d-flex justify-content-center">
            <div class="card-body">
                <h5 class="card-title text-center mb-3">Conserved moments</h5>
                <p class="card-text text-center fs-1">{% for c in consm
                    %} ${{
                    c }}$ {% endfor %}
                </p>
            </div>
        </div>
    </div>

    <div class="accordion" id="accordionScheme">
        {%- for k in range(scheme.nschemes) %}
        <div class="accordion-item">
            <h2 class="accordion-header" id="heading{{k}}">
                <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse"
                    data-bs-target="#collapse{{k}}" aria-expanded="false" aria-controls="collapse{{k}}">
                    {{ header_scheme[k] }}
                </button>
            </h2>
            <div id="collapse{{k}}" class="accordion-collapse collapse" aria-labelledby="heading{{k}}"
                data-bs-parent="#accordionScheme">
                <div class="accordion-body">
                    <span class="d-block p-2 border-bottom border-2">Velocities</span>

                    <img class="w-50 mx-auto d-block" src="data:image/png;base64,{{ fig[k] }}" />

                    <span class="d-block p-2 border-bottom border-2">Polynomials</span>
                    {% for p in P[k] %}
                    $${{ p }}$$
                    {% endfor %}

                    <span class="d-block p-2 border-bottom border-2">Equilibria</span>
                    {% for e in EQ[k] %}
                    $${{ e }}$$
                    {% endfor %}

                    <span class="d-block p-2 border-bottom border-2">Relaxation parameters</span>
                    {% for sk in s[k] %}
                    $${{ sk }}$$
                    {% endfor %}
                </div>
            </div>
        </div>
        {%- endfor %}

        <div class="accordion-item">
            <h2 class="accordion-header" id="headingMoment">
                <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse"
                    data-bs-target="#collapseMoment" aria-expanded="false" aria-controls="collapseMoment">
                    Moments matrix
                </button>
            </h2>
            <div id="collapseMoment" class="accordion-collapse collapse" aria-labelledby="headingMoment"
                data-bs-parent="#accordionScheme">
                <div class="accordion-body">
                    $$\displaystyle{ {{ M }} }$$
                </div>
            </div>
        </div>

        <div class="accordion-item">
            <h2 class="accordion-header" id="headingInvMoment">
                <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse"
                    data-bs-target="#collapseInvMoment" aria-expanded="false" aria-controls="collapseInvMoment">
                    Inverse of moments matrix
                </button>
            </h2>
            <div id="collapseInvMoment" class="accordion-collapse collapse" aria-labelledby="headingInvMoment"
                data-bs-parent="#accordionScheme">
                <div class="accordion-body">
                    $$\displaystyle{ {{ invM }} }$$
                </div>
            </div>
        </div>

    </div>
</div>

<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/js/bootstrap.bundle.min.js"
    integrity="sha384-ygbV9kiqUc6oa4msXn9868pTtWMgiQaeYH7/t7LECLbyPA2x65Kgf80OJFdroafW"
    crossorigin="anonymous"></script>
<script>
    MathJax = {
        tex: {
            inlineMath: [['$', '$'], ['\\(', '\\)']]
        }
    };
</script>
<script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js">
</script>'