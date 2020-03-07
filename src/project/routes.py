from views import (
    index,
    list_employee,
    get_employee,
    create_employee,
    update_employee,

    list_car,
    get_car,
    create_car,
    update_car,

    list_spares,
    list_spares_with_car,
    get_spares,
    create_spares,
    update_spares,
)


def setup_routes(app):
    # EMPLOYEE ROUTES
    app.router.add_route('GET', '/', index)
    app.router.add_route('GET', '/employee/', list_employee)
    app.router.add_route('GET', '/employee/{id:\d+}/', get_employee)
    app.router.add_route('POST', '/employee/', create_employee)
    app.router.add_route('PUT', '/employee/{id:\d+}/', update_employee)

    # CAR ROUTES
    app.router.add_route('GET', '/car/', list_car)
    app.router.add_route('GET', '/car/{id:\d+}/', get_car)
    app.router.add_route('POST', '/car/', create_car)
    app.router.add_route('PUT', '/car/{id:\d+}/', update_car)

    # SPARES ROUTES
    app.router.add_route('GET', '/spares/', list_spares)
    app.router.add_route('GET', '/spares_with_car/', list_spares_with_car)
    app.router.add_route('GET', '/spares/{id:\d+}/', get_spares)
    app.router.add_route('POST', '/spares/', create_spares)
    app.router.add_route('PUT', '/spares/{id:\d+}/', update_spares)